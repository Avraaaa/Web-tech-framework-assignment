from flask import jsonify, request
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    status = 400
    title = "Bad Request"

    def __init__(self, detail, errors=None):
        super().__init__(detail)
        self.detail = detail
        self.errors = errors


class ValidationError(ApiError):
    status = 422
    title = "Validation Failed"


class NotFoundError(ApiError):
    status = 404
    title = "Not Found"


class ConflictError(ApiError):
    status = 409
    title = "Conflict"


def problem(status, title, detail, errors=None):
    body = {
        "type": "about:blank",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": request.path,
    }
    if errors:
        body["errors"] = errors
    response = jsonify(body)
    response.status_code = status
    response.content_type = "application/problem+json"
    return response


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(e):
        return problem(e.status, e.title, e.detail, e.errors)

    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        return problem(e.code, e.name, e.description)

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        app.logger.exception("Unhandled error")
        return problem(500, "Internal Server Error", "An unexpected error occurred")
