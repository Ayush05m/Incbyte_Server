import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_registration():
    response = client.post("/users/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201  # Expecting 201 Created
    assert "id" in response.json()

def test_user_login():
    response = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200  # Expecting 200 OK
    assert "access_token" in response.json()
