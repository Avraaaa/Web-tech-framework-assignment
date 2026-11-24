from dataclasses import dataclass, asdict


@dataclass
class Organization:
    id: int
    name: str
    contact_email: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ServiceRequest:
    id: int
    title: str
    description: str
    organization: int
    priority: str
    status: str = "DRAFT"

    def to_dict(self):
        return asdict(self)
