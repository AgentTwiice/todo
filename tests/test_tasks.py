from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine

from backend.app.main import app
from backend.app import database


def setup_module(module):
    database.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(database.engine)


def get_client():
    return TestClient(app)


def auth_headers(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "pass"})
    login = client.post("/auth/login", json={"email": "user@example.com", "password": "pass"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_list_update_complete_delete():
    client = get_client()
    headers = auth_headers(client)

    due = (datetime.utcnow() + timedelta(days=1)).isoformat()
    r = client.post("/tasks/", json={"title": "Task 1", "due_datetime": due}, headers=headers)
    assert r.status_code == 200
    task = r.json()
    task_id = task["id"]

    r = client.get("/tasks/?limit=1&offset=0", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1

    r = client.put(f"/tasks/{task_id}", json={"title": "Updated"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

    r = client.post(f"/tasks/{task_id}/complete", headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "completed"

    r = client.delete(f"/tasks/{task_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_due_date_validation():
    client = get_client()
    headers = auth_headers(client)
    past_due = (datetime.utcnow() - timedelta(days=1)).isoformat()
    r = client.post("/tasks/", json={"title": "Invalid", "due_datetime": past_due}, headers=headers)
    assert r.status_code == 400
