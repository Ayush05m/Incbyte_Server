import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_purchase():
    response = client.post("/purchases/", json={"user_id": 1, "sweet_id": 1, "quantity": 2})
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_purchases():
    response = client.get("/purchases/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
