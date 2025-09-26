import sys
import asyncio
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import pytest
import random
import string
import httpx
from httpx import ASGITransport
from sqlalchemy.orm import Session
from app.models.user import User
from app.main import app
from app.models.sweet import Sweet
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.db.session import AsyncSessionLocal
from unittest.mock import patch, MagicMock
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

def random_email():
    return f"test_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@example.com"

import pytest
from fastapi import FastAPI
from app.main import app

API_V1_STR = "/api"

@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def test_user(db: AsyncSession) -> User:
    email = random_email()
    user_in = UserCreate(username=email, email=email, password="password", full_name="Test User")
    user = await create_user(db, user_in)
    return user

@pytest.fixture(scope="function")
async def test_admin(db: AsyncSession) -> User:
    email = random_email()
    user_in = UserCreate(username=email, email=email, password="password", full_name="Admin User", role="admin")
    user = await create_user(db, user_in)
    return user

@pytest.fixture(scope="function")
async def auth_headers(test_user: User):
    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.post(f"{API_V1_STR}/auth/login", json={"email": test_user.email, "password": "password"})
        access_token = response.json()["data"]["access_token"]
        return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
async def admin_auth_headers(test_admin: User):
    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.post(f"{API_V1_STR}/auth/login", json={"email": test_admin.email, "password": "password"})
        access_token = response.json()["data"]["access_token"]
        return {"Authorization": f"Bearer {access_token}"}

async def test_create_sweet(db: AsyncSession, admin_auth_headers: dict):
    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.post(f"{API_V1_STR}/sweets/", headers=admin_auth_headers, data={"name": "Test Sweet", "category": "Test", "description": "Test desc", "price": 10.0, "quantity": 100})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Sweet created successfully"
        assert data["data"]["name"] == "Test Sweet"

async def test_read_sweets(db: AsyncSession, auth_headers: dict):
    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.get(f"{API_V1_STR}/sweets/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Sweets fetched successfully"
        assert isinstance(data["data"], list)

async def test_search_sweets(db: AsyncSession, auth_headers: dict):
    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.get(f"{API_V1_STR}/sweets/search?name=Test", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Sweets search successful"
        assert isinstance(data["data"], list)

async def test_update_sweet(db: AsyncSession, admin_auth_headers: dict):
    sweet = Sweet(name="Update Sweet", price=10.0, quantity=100, category="Test")
    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)

    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.put(f"{API_V1_STR}/sweets/{sweet.id}", headers=admin_auth_headers, data={"name": "Updated Sweet"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Sweet updated successfully"
        assert data["data"]["name"] == "Updated Sweet"

async def test_delete_sweet(db: AsyncSession, admin_auth_headers: dict):
    sweet = Sweet(name="Delete Sweet", price=10.0, quantity=100, category="Test")
    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)

    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.delete(f"{API_V1_STR}/sweets/{sweet.id}", headers=admin_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Delete Sweet"

@patch('app.api.routes.sweets.create_razorpay_order')
async def test_purchase_sweet(mock_create_razorpay_order: MagicMock, db: AsyncSession, auth_headers: dict):
    mock_create_razorpay_order.return_value = {"id": "order_123", "amount": 1000, "currency": "INR"}
    sweet = Sweet(name="Purchase Sweet", price=10.0, quantity=100, category="Test")
    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)

    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.post(f"{API_V1_STR}/sweets/{sweet.id}/purchase", headers=auth_headers, json={"quantity": 1})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Razorpay order created"
        assert data["data"]["order_id"] == "order_123"

@patch('app.api.routes.sweets.verify_razorpay_payment')
async def test_verify_payment(mock_verify_razorpay_payment: MagicMock, db: AsyncSession, auth_headers: dict):
    mock_verify_razorpay_payment.return_value = True
    sweet = Sweet(name="Verify Sweet", price=10.0, quantity=100, category="Test")
    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)

    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.post(f"{API_V1_STR}/sweets/{sweet.id}/verify_payment", headers=auth_headers, json={"razorpay_order_id": "order_123", "razorpay_payment_id": "pay_123", "razorpay_signature": "sig_123"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Payment successful"
        assert data["data"]["payment_id"] == "pay_123"

async def test_restock_sweet(db: AsyncSession, admin_auth_headers: dict):
    sweet = Sweet(name="Restock Sweet", price=10.0, quantity=100, category="Test")
    db.add(sweet)
    await db.commit()
    await db.refresh(sweet)

    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.put(f"{API_V1_STR}/sweets/{sweet.id}/restock", headers=admin_auth_headers, json={"quantity": 50})
        assert response.status_code == 200
        data = response.json()
        assert data["quantity"] == 150

import pytest

@pytest.mark.asyncio
async def test_create_sweet():
    email = random_email()
    async with AsyncSessionLocal() as db:
        user_in = UserCreate(username=email, email=email, password="password", full_name="Test User")
        user = await create_user(db, user_in)
    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        login_response = await ac.post(f"{API_V1_STR}/auth/login", json={"email": email, "password": "password"})
        login_json = login_response.json()
        assert login_response.status_code == 200, f"Login failed: {login_json}"
        assert "data" in login_json, f"Login response missing 'data': {login_json}"
        access_token = login_json["data"]["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        sweet_response = await ac.post(f"{API_V1_STR}/sweets/", headers=headers, data={"name": "Ladoo", "category": "Test", "description": "desc", "price": 10, "quantity": 10})
        sweet_json = sweet_response.json()
        assert sweet_response.status_code in [200, 201], f"Sweet creation failed: {sweet_json}"
        assert "data" in sweet_json

@pytest.mark.asyncio
async def test_get_sweets():
    email = random_email()
    async with AsyncSessionLocal() as db:
        user_in = UserCreate(username=email, email=email, password="password", full_name="Test User")
        user = await create_user(db, user_in)
    async with httpx.AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        login_response = await ac.post(f"{API_V1_STR}/auth/login", json={"email": email, "password": "password"})
        login_json = login_response.json()
        assert login_response.status_code == 200, f"Login failed: {login_json}"
        assert "data" in login_json, f"Login response missing 'data': {login_json}"
        access_token = login_json["data"]["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        sweets_response = await ac.get(f"{API_V1_STR}/sweets/", headers=headers)
        sweets_json = sweets_response.json()
        assert sweets_response.status_code == 200, f"Get sweets failed: {sweets_json}"
        assert "data" in sweets_json