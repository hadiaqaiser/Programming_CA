# simple pytest test for my first flask route /api/ping
import pytest
from backend.app import app

# use flask test_client to check response code + message
def test_ping_route():
    client = app.test_client()
    res = client.get("/api/ping")
    data = res.get_json()

    assert res.status_code == 200
    assert data["message"] == "medoracare api ok"