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
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            if User.query.filter_by(email=email).first():
                return jsonify({'message': 'Email already registered'}), 400
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('registerForm.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, app.config['SECRET_KEY'])
                session['token'] = token
                return redirect(url_for('dashboard'))
            return jsonify({'message': 'Invalid credentials'}), 401
        return render_template('login.html')

    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        token = session.get('token')
        if not token:
            return redirect(url_for('login'))
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
            return redirect(url_for('dashboard'))
        
        messages = Message.query.filter((Message.sender_id == data['user_id']) | (Message.receiver_id == data['user_id'])).all()
        return render_template('chatInterface.html', messages=messages)

    @app.route('/logout')
    def logout():
        session.pop('token', None)
        return redirect(url_for('login'))
