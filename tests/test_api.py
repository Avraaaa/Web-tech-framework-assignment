def make_organization(client):
    body = {"name": "Northbridge Bank", "contact_email": "it@northbridge.example"}
    return client.post("/api/organizations", json=body).get_json()["id"]


def request_body(organization, **overrides):
    body = {"title": "Login fails", "description": "Error on submit", "organization": organization, "priority": "HIGH"}
    body.update(overrides)
    return body


def test_organization_crud(client):
    r = client.post("/api/organizations", json={"name": "Northbridge Bank", "contact_email": "it@northbridge.example"})
    assert r.status_code == 201
    oid = r.get_json()["id"]
    assert client.get("/api/organizations").get_json()[0]["name"] == "Northbridge Bank"
    assert client.get(f"/api/organizations/{oid}").status_code == 200
    r = client.put(f"/api/organizations/{oid}", json={"name": "Meghna Bank", "contact_email": "ops@meghna.example"})
    assert r.get_json()["name"] == "Meghna Bank"
    assert client.delete(f"/api/organizations/{oid}").status_code == 204
    assert client.get(f"/api/organizations/{oid}").status_code == 404


def test_service_request_crud(client):
    oid = make_organization(client)
    r = client.post("/api/service-requests", json=request_body(oid))
    assert r.status_code == 201
    sid = r.get_json()["id"]
    assert r.get_json()["status"] == "DRAFT"
    assert len(client.get("/api/service-requests").get_json()) == 1
    assert client.get(f"/api/service-requests/{sid}").get_json()["title"] == "Login fails"
    r = client.put(f"/api/service-requests/{sid}", json=request_body(oid, priority="LOW"))
    assert r.get_json()["priority"] == "LOW"
    assert client.delete(f"/api/service-requests/{sid}").status_code == 204
    assert client.get(f"/api/service-requests/{sid}").status_code == 404


def test_validation_returns_422_problem(client):
    r = client.post("/api/organizations", json={"name": "", "contact_email": "not-an-email"})
    assert r.status_code == 422
    assert r.content_type == "application/problem+json"
    body = r.get_json()
    assert body["status"] == 422 and set(body["errors"]) == {"name", "contact_email"}
    r = client.post("/api/service-requests", json=request_body(999, priority="URGENT"))
    assert r.status_code == 422 and set(r.get_json()["errors"]) == {"organization", "priority"}


def test_not_found_returns_404_problem(client):
    r = client.get("/api/service-requests/999")
    assert r.status_code == 404
    assert r.get_json()["title"] == "Not Found"
    assert client.delete("/api/organizations/999").status_code == 404


def test_submitted_request_cannot_be_deleted(client):
    oid = make_organization(client)
    sid = client.post("/api/service-requests", json=request_body(oid, status="SUBMITTED")).get_json()["id"]
    r = client.delete(f"/api/service-requests/{sid}")
    assert r.status_code == 409
    assert r.content_type == "application/problem+json"
    assert client.get(f"/api/service-requests/{sid}").status_code == 200


def test_request_id_header(client):
    assert client.get("/api/organizations").headers["X-Request-ID"]
    assert client.get("/api/organizations", headers={"X-Request-ID": "abc"}).headers["X-Request-ID"] == "abc"
