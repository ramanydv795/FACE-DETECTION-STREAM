import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock database before importing app
with patch('database.create_engine'), \
     patch('database.Base.metadata.create_all'):
    from main import app

client = TestClient(app)

# ── Helper ──
def get_auth_token():
    response = client.get("/token")
    return response.json()["access_token"]

# ── Test 1: Root ──
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Face Detection API Running!"

# ── Test 2: Health ──
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# ── Test 3: Token generation ──
def test_get_token():
    response = client.get("/token")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# ── Test 4: ROI without auth ──
def test_roi_without_auth():
    response = client.get("/roi")
    assert response.status_code == 401

# ── Test 5: ROI with auth ──
def test_roi_with_auth():
    token = get_auth_token()
    mock_db = MagicMock()
    mock_db.query.return_value.order_by.return_value.limit.return_value.all.return_value = []
    
    with patch('main.get_db', return_value=iter([mock_db])):
        response = client.get(
            "/roi",
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert "roi_data" in response.json()

# ── Test 6: Invalid token ──
def test_roi_invalid_token():
    response = client.get(
        "/roi",
        headers={"Authorization": "Bearer invalidtoken123"}
    )
    assert response.status_code == 401

# ── Test 7: Token is valid JWT ──
def test_token_is_valid_jwt():
    from auth import verify_token
    from fastapi.security import HTTPAuthorizationCredentials
    
    token = get_auth_token()
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )
    payload = verify_token(credentials)
    assert payload["sub"] == "demo-user"