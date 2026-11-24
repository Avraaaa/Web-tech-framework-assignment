# Architecture

Request flow: `HTTP -> middleware (request ID, logging) -> controller -> service -> repository -> in-memory dict`

| Layer | File | Responsibility |
|---|---|---|
| Config | `app/config.py` | Reads `APP_ENV`, `LOG_LEVEL`, `PORT` from the environment |
| Controllers | `app/controllers.py` | Routes, HTTP parsing, status codes |
| Services | `app/services.py` | Validation (422) and business rules (409) |
| Repositories | `app/repositories.py` | In-memory storage |
| Domain models | `app/models.py` | `Organization`, `ServiceRequest` dataclasses |
| Errors | `app/errors.py` | Centralized RFC 9457 problem details |
| App factory | `app/__init__.py` | Wires layers, request IDs and logging |

Business rule: a service request with status `SUBMITTED` cannot be deleted (409 Conflict).

Controllers never touch storage directly; services never touch HTTP. Swapping the in-memory repository for a database only changes the repository layer.
