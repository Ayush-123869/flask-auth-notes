class APIError(Exception):
    """Base class for custom API errors"""
    def __init__(self, message, status_code=400, details=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.details = details

class ValidationError(APIError):
    def __init__(self, message="Validation failed", details=None):
        super().__init__(message, status_code=400, details=details)

class AuthError(APIError):
    def __init__(self, message="Authentication failed", details=None):
        super().__init__(message, status_code=401, details=details)

class AuthorizationError(APIError):
    def __init__(self, message="Not authorized to access this resource", details=None):
        super().__init__(message, status_code=403, details=details)

class NotFoundError(APIError):
    def __init__(self, message="Resource not found", details=None):
        super().__init__(message, status_code=404, details=details)

class ConflictError(APIError):
    def __init__(self, message="Resource conflict", details=None):
        super().__init__(message, status_code=409, details=details)
