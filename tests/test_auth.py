from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine

from backend.app.main import app
from backend.app import database


def setup_module(module):
    database.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(database.engine)


def get_client():
    return TestClient(app)


def test_register_and_login():
    client = get_client()
    r = client.post("/auth/register", json={"email": "user@example.com", "password": "pass"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    r = client.post("/auth/login", json={"email": "user@example.com", "password": "pass"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_google_callback():
    client = get_client()
    client.post("/auth/register", json={"email": "foo@example.com", "password": "pass"})
    login = client.post("/auth/login", json={"email": "foo@example.com", "password": "pass"})
    token = login.json()["access_token"]
    r = client.get("/auth/google/callback?code=abc", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["access_token"] == "abc_access"
