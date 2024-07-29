from flask import Flask
from configuration import Config
from extensions import db
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)




