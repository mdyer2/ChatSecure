import os
from application import app, db
from model import User, Message

# Path to the SQLite database file
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'application.db')

# Remove the existing SQLite database file
if os.path.exists(db_path):
    os.remove(db_path)

with app.app_context():
    # Drop all the tables
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("Tables created")

    # Create a new user
    user = User(username='john_doe', email='john@example.com')
    user.set_password('mypassword')
    db.session.add(user)
    db.session.commit()

    # Verify password
    print(user.check_password('mypassword'))  # Should print True

    # Create a new message
    message = Message(sender_id=user.id, receiver_id=2, content='Hello, World!')
    db.session.add(message)
    db.session.commit()

    # Print message
    print(message)
