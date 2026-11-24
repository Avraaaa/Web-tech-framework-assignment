from app.models import Organization, ServiceRequest

ORGANIZATIONS = [
    ("Northbridge Bank PLC", "itsupport@northbridgebank.com.bd"),
    ("Riverstone Commercial Bank", "servicedesk@riverstonebank.com.bd"),
    ("Coastal Finance Limited", "operations@coastalfinance.com.bd"),
]

SERVICE_REQUESTS = [
    ("Fund transfer fails after OTP confirmation", "Customers receive error TXN-504 after confirming an interbank transfer with OTP. Observed on internet banking v4.2 since 18 November.", 1, "CRITICAL", "SUBMITTED"),
    ("Monthly statement columns overlap in PDF", "Debit and credit columns overlap when the account statement is exported to PDF for accounts with more than 200 transactions.", 1, "LOW", "DRAFT"),
    ("Login OTP delayed for some mobile operators", "Branch staff report that login OTP SMS arrives 3 to 5 minutes late for a subset of customers.", 2, "HIGH", "SUBMITTED"),
    ("Add EMI breakdown to loan application screen", "Show monthly installment, total interest and tenure before the officer submits a personal loan application.", 3, "MEDIUM", "DRAFT"),
    ("Branch report export times out", "The daily branch transaction report times out when the date range exceeds 31 days.", 3, "HIGH", "SUBMITTED"),
]


def seed(organizations, service_requests):
    for name, contact_email in ORGANIZATIONS:
        organizations.save(Organization(organizations.next_id(), name, contact_email))
    for title, description, organization, priority, status in SERVICE_REQUESTS:
        service_requests.save(
            ServiceRequest(service_requests.next_id(), title, description, organization, priority, status)
        )
