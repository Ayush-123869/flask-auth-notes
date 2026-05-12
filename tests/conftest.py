import pytest
from app import create_app
from app.extensions import db
from app.config.settings import TestConfig
from app.models.user import User
from app.extensions import bcrypt
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    with app.app_context():
        password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
        user = User(username='testuser', email='test@test.com', password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()

@pytest.fixture
def auth_headers(app, test_user):
    with app.app_context():
        # Get the actual user ID from the dict returned by fixture
        token = create_access_token(identity=test_user['id'])
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
