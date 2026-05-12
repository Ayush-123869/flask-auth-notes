from app.models.user import User
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token
from app.utils.errors import ValidationError, ConflictError, AuthError

class AuthService:
    @staticmethod
    def register_user(data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            raise ValidationError("Username, email, and password are required")

        if User.query.filter_by(username=username).first():
            raise ConflictError("Username already exists")

        if User.query.filter_by(email=email).first():
            raise ConflictError("Email already exists")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        return new_user.to_dict()

    @staticmethod
    def login_user(data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise ValidationError("Username and password are required")

        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            raise AuthError("Invalid username or password")

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}
