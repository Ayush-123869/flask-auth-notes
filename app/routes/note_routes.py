from flask import Blueprint, request
from app.services.note_service import NoteService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.responses import success_response

note_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@note_bp.route('/', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    data = NoteService.get_all_notes(user_id, request.args)
    return success_response(data=data, message="Notes retrieved successfully")

@note_bp.route('/', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    note_data = NoteService.create_note(user_id, data)
    return success_response(data=note_data, message="Note created successfully", status_code=201)

@note_bp.route('/<note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    user_id = get_jwt_identity()
    note_data = NoteService.get_note_by_id(user_id, note_id)
    return success_response(data=note_data, message="Note retrieved successfully")

@note_bp.route('/<note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    note_data = NoteService.update_note(user_id, note_id, data)
    return success_response(data=note_data, message="Note updated successfully")

@note_bp.route('/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    NoteService.delete_note(user_id, note_id)
    return success_response(message="Note deleted successfully")
