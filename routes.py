from flask import request, jsonify, render_template, redirect, url_for, session
import jwt
from datetime import datetime, timedelta
from models import User, Message
from extensions import db

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('homepageIndex.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                
                if not username or not email or not password:
                    return jsonify({'message': 'All fields are required'}), 400
                
                if User.query.filter_by(email=email).first():
                    return jsonify({'message': 'Email already registered'}), 400
                
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                
                return jsonify({'message': 'User registered successfully'}), 201
            else:
                return jsonify({'message': 'Invalid content type, expected application/json'}), 415
        return render_template('registerForm.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                email = data.get('email')
                password = data.get('password')
                
                if not email or not password:
                    return jsonify({'message': 'All fields are required'}), 400
                
                user = User.query.filter_by(email=email).first()
                if user and user.check_password(password):
                    token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, app.config['SECRET_KEY'])
                    return jsonify({'token': token, 'redirect_url': url_for('dashboard')}), 200
                return jsonify({'message': 'Invalid credentials'}), 401
            else:
                return jsonify({'message': 'Invalid content type, expected application/json'}), 415
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 403

        messages = Message.query.filter((Message.sender_id == data['user_id']) | (Message.receiver_id == data['user_id'])).all()
        return render_template('chatInterface.html', messages=messages)

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        users_list = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(users_list)

    @app.route('/send_message', methods=['POST'])
    def send_message():
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 403

        user_id = data['user_id']
        data = request.get_json()
        content = data['content']
        new_message = Message(sender_id=user_id, content=content)
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'}), 201

    @app.route('/get_messages', methods=['GET'])
    def get_messages():
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 403

        user_id = data['user_id']
        messages = Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).all()
        return jsonify([{'sender_id': msg.sender_id, 'receiver_id': msg.receiver_id, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages])
