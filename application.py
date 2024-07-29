from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db
from configuration import Config
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

# Use ProxyFix to handle proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

# Initialize the database
db.init_app(app)

# Register routes
register_routes(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)



