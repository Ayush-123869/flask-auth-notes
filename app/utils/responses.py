from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    response = {
        "success": True,
        "message": message,
    }
    if data is not None:
        response["data"] = data
        
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, details=None):
    response = {
        "success": False,
        "error": {
            "message": message,
        }
    }
    if details is not None:
        response["error"]["details"] = details
        
    return jsonify(response), status_code
