import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_login():
    response = client.post("/auth/login", data={"email": "demo@demo.demo", "password": "password"})
    assert response.status_code == 401  # Unauthorized
    assert response.json()["detail"] == "Invalid credentials"
