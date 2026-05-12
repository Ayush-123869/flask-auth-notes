from flask import Flask
from app.config.settings import Config
from app.extensions import db, migrate, jwt, bcrypt
from app.routes import register_blueprints
from app.models import User, Note # Ensure models are known to SQLAlchemy/Flask-Migrate
from app.middleware.error_handler import register_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register Error Handlers
    register_error_handlers(app)

    # Register Blueprints
    register_blueprints(app)

    @app.route('/health')
    def health_check():
        return {"status": "healthy"}, 200

    return app
