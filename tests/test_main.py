# Local imports
from tests.conftest import headers


def test_authentication(client):
    # Check that the API is accessible
    resp = client.get("/api/v1/status")
    assert resp.status_code == 200
    assert resp.json["message"] == "Up and running"

    # Check the auth route without a key
    resp = client.get("/api/v1/auth")
    assert resp.status_code == 401
    assert resp.json["error"] == "Not authorized"

    # Check auth route with incorrect key
    resp = client.get("/api/v1/auth", headers={"Authorization": "Bearer foo"})
    assert resp.status_code == 401
    assert resp.json["error"] == "A valid authorization token is required"

    # Check auth route with the correct key
    resp = client.get("/api/v1/auth", headers=headers)
    assert resp.status_code == 200
    assert resp.json["message"] == "API token is valid"


def test_demo(client):
    # Run the demo without a key
    resp = client.get("/api/v1/demo")
    assert resp.status_code == 401
    assert resp.json["error"] == "Not authorized"

    # Run the api/v1/demo with a key
    resp = client.get("/api/v1/demo", headers=headers)
    assert resp.status_code == 200
    assert resp.json["message"] == "Hello World!"

    # Run the api/v1/demo with a name as a query param
    resp = client.get("/api/v1/demo?name=pytest", headers=headers)
    assert resp.status_code == 200
    assert resp.json["message"] == "Hello pytest!"

    # Run the api/v1/demo with a name in the body
    resp = client.post("/api/v1/demo", headers=headers, json={"name": "pytest"})
    assert resp.status_code == 200
    assert resp.json["message"] == "Hello pytest!"

    # Run the api/v1/demo with the name in both body and query param
    resp = client.get(
        "/api/v1/demo?name=pytest", headers=headers, json={"name": "pytest"}
    )
    assert resp.status_code == 200
    assert resp.json["message"] == "Hello pytest!"
