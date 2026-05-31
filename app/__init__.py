from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)

    # Initialize database
    with app.app_context():
        from .models import init_db
        init_db()

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app