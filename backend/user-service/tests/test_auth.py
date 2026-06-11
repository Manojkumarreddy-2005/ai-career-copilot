# 1. Force Python to find and load your .env file before anything else runs
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# 2. Your original test setup continues exactly the same below
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post("/auth/register", json={
        "email": "newuser@test.com",
        "password": "testpass123",
        "first_name": "Jane",
        "last_name": "Doe"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "newuser@test.com"

def test_login():
    # Register first
    client.post("/auth/register", json={
        "email": "loginuser@test.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    })
    # Then login
    response = client.post("/auth/login", json={
        "email": "loginuser@test.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    response = client.post("/auth/login", json={
        "email": "nobody@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401