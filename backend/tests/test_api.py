import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_validation() -> None:
    response = client.post("/generate", json={})
    assert response.status_code == 422


def test_agent_run_validation() -> None:
    response = client.post("/agent/run", json={})
    assert response.status_code == 422


def test_agent_run_with_prompt() -> None:
    response = client.post("/agent/run", json={"prompt": "Write a hello world function"})
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "reasoning" in data
    assert "attempts" in data
    assert "status" in data
