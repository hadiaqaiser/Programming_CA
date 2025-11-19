# fix python path so pytest can import backend module
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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