import logging
import uuid

from flask import Flask, g, request

from app.config import Config
from app.controllers import crud_blueprint
from app.errors import register_error_handlers
from app.repositories import InMemoryRepository
from app.services import OrganizationService, ServiceRequestService


def create_app(config=None):
    config = config or Config()
    app = Flask(__name__)
    app.config.from_object(config)
    logging.basicConfig(level=config.LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")

    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

    @app.after_request
    def log_and_tag(response):
        response.headers["X-Request-ID"] = g.get("request_id", "")
        app.logger.info("%s %s %s %s", g.get("request_id"), request.method, request.path, response.status_code)
        return response

    register_error_handlers(app)
    organizations = InMemoryRepository()
    app.register_blueprint(crud_blueprint("organizations", "/api/organizations", OrganizationService(organizations)))
    app.register_blueprint(
        crud_blueprint("service_requests", "/api/service-requests", ServiceRequestService(InMemoryRepository(), organizations))
    )
    return app
