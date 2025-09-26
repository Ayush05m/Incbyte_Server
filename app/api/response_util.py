def standard_response(success: bool, message: str = None, data = None, error = None):
    return {
        "success": success,
        "message": message,
        "data": data,
        "error": error
    }
