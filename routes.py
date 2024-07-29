
from flask import request, jsonify, render_template_string, redirect, url_for, session
import jwt
from datetime import datetime, timedelta
from models import User, Message
from extensions import db

def register_routes(app):
    @app.route('/')
    def index():
        return render_template_string(open('homepageIndex.html').read())

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            data = request.get_json()
            username = data['username']
            email = data['email']
            password = data['password']
            if User.query.filter_by(email=email).first():
                return jsonify({'message': 'Email already registered'}), 400
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        return render_template_string(open('registerForm.html').read())

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.get_json()
            email = data['email']
            password = data['password']
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, app.config['SECRET_KEY'])
                return jsonify({'token': token})
            return jsonify({'message': 'Invalid credentials'}), 401
        return render_template_string(open('login.html').read())

    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403

        if request.method == 'POST':
            receiver_id = request.form['receiver_id']
            content = request.form['message']
            new_message = Message(sender_id=data['user_id'], receiver_id=receiver_id, content=content)
            db.session.add(new_message)
            db.session.commit()
            return jsonify({'message': 'Message sent successfully'}), 201
        
        messages = Message.query.filter((Message.sender_id == data['user_id']) | (Message.receiver_id == data['user_id'])).all()
        return render_template_string(open('chatInterface.html').read(), messages=messages)

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        users_list = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(users_list)
