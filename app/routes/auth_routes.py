from flask import Blueprint, request
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.responses import success_response

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_data = AuthService.register_user(data)
    return success_response(data={"user": user_data}, message="User created successfully", status_code=201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token_data = AuthService.login_user(data)
    return success_response(data=token_data, message="Login successful", status_code=200)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    return success_response(data={"user_id": current_user_id}, message="Protected route accessed", status_code=200)
