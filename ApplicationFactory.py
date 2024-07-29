from flask import Flask
from configuration import Config
from extensions import db
from routes import register_routes

def create_app():
    # Create the Flask application
    app = Flask(__name__)
    
    # Load the configuration from the Config class
    app.config.from_object(Config)
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Register routes
    register_routes(app)

    return app
