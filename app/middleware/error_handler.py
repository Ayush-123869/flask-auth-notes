from flask import json
from werkzeug.exceptions import HTTPException
from app.utils.errors import APIError
from app.utils.responses import error_response

def register_error_handlers(app):
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return error_response(message=error.message, status_code=error.status_code, details=error.details)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle standard HTTP exceptions (like 404, 405) properly as JSON"""
        return error_response(message=error.description, status_code=error.code)

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Catch-all for unhandled exceptions (500)"""
        # In production, log the actual error stack trace here
        return error_response(message="An internal server error occurred", status_code=500)

    # JWT Specific errors can be handled here if they raise exceptions,
    # or by registering Flask-JWT-Extended error callbacks inside app factory.
