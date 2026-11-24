# SPL-2 Backend

Standalone Flask backend for client organizations and service requests (QFD N-02, N-06), based on the SPL-2 prototype. Data is held in memory.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && export $(cat .env | xargs)
python run.py
```

Open http://127.0.0.1:5000 for the frontend.

## Test

```bash
pytest -q
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET / POST | `/api/organizations` | List / create client organizations |
| GET / PUT / DELETE | `/api/organizations/<id>` | Read / update / delete an organization |
| GET / POST | `/api/service-requests` | List / create service requests |
| GET / PUT / DELETE | `/api/service-requests/<id>` | Read / update / delete a service request |

Organization body: `{"name": "Northbridge Bank", "contact_email": "it@northbridge.example"}`
Service request body: `{"title": "Login fails", "description": "Error on submit", "organization": 1, "priority": "HIGH", "status": "DRAFT"}`

Errors use RFC 9457 `application/problem+json`: 422 validation, 404 not found, 409 deleting a `SUBMITTED` service request. Every response carries an `X-Request-ID` header.
