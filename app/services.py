import re

from app.errors import ConflictError, NotFoundError, ValidationError
from app.models import Organization, ServiceRequest

STATUSES = ("DRAFT", "SUBMITTED")
PRIORITIES = ("LOW", "MEDIUM", "HIGH", "CRITICAL")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _require_object(data):
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")


def _require_text(data, field, errors, max_length):
    value = data.get(field)
    if not isinstance(value, str) or not value.strip() or len(value) > max_length:
        errors[field] = f"must be a non-empty string up to {max_length} characters"


class OrganizationService:
    def __init__(self, repo):
        self.repo = repo

    def _validate(self, data):
        _require_object(data)
        errors = {}
        _require_text(data, "name", errors, 160)
        if not isinstance(data.get("contact_email"), str) or not EMAIL.match(data["contact_email"]):
            errors["contact_email"] = "must be a valid email address"
        if errors:
            raise ValidationError("Invalid organization", errors)

    def list(self):
        return self.repo.list()

    def get(self, item_id):
        item = self.repo.get(item_id)
        if not item:
            raise NotFoundError(f"Organization {item_id} not found")
        return item

    def create(self, data):
        self._validate(data)
        return self.repo.save(Organization(self.repo.next_id(), data["name"].strip(), data["contact_email"].strip()))

    def update(self, item_id, data):
        item = self.get(item_id)
        self._validate(data)
        item.name = data["name"].strip()
        item.contact_email = data["contact_email"].strip()
        return self.repo.save(item)

    def delete(self, item_id):
        self.get(item_id)
        self.repo.delete(item_id)


class ServiceRequestService:
    def __init__(self, repo, organizations):
        self.repo = repo
        self.organizations = organizations

    def _validate(self, data):
        _require_object(data)
        errors = {}
        _require_text(data, "title", errors, 200)
        _require_text(data, "description", errors, 5000)
        if data.get("priority") not in PRIORITIES:
            errors["priority"] = f"must be one of {list(PRIORITIES)}"
        if data.get("status", "DRAFT") not in STATUSES:
            errors["status"] = f"must be one of {list(STATUSES)}"
        organization = data.get("organization")
        if isinstance(organization, bool) or not isinstance(organization, int) or not self.organizations.get(organization):
            errors["organization"] = "must be an existing organization id"
        if errors:
            raise ValidationError("Invalid service request", errors)

    def list(self):
        return self.repo.list()

    def get(self, item_id):
        item = self.repo.get(item_id)
        if not item:
            raise NotFoundError(f"Service request {item_id} not found")
        return item

    def create(self, data):
        self._validate(data)
        item = ServiceRequest(
            self.repo.next_id(),
            data["title"].strip(),
            data["description"].strip(),
            data["organization"],
            data["priority"],
            data.get("status", "DRAFT"),
        )
        return self.repo.save(item)

    def update(self, item_id, data):
        item = self.get(item_id)
        self._validate(data)
        item.title = data["title"].strip()
        item.description = data["description"].strip()
        item.organization = data["organization"]
        item.priority = data["priority"]
        item.status = data.get("status", item.status)
        return self.repo.save(item)

    def delete(self, item_id):
        item = self.get(item_id)
        if item.status == "SUBMITTED":
            raise ConflictError("A submitted service request cannot be deleted")
        self.repo.delete(item_id)
