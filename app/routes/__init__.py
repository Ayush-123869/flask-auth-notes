from .auth_routes import auth_bp
from .note_routes import note_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(note_bp)
