import pytest
from fastapi.testclient import TestClient
from backend.main import app  # Обновленный путь импорта

client = TestClient(app)

def test_login_success():
    response = client.post("/api/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    response = client.post("/api/login", json={"email": "wrong@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
