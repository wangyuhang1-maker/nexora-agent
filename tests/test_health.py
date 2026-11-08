"""Step 1 acceptance tests: the app starts and the health endpoint works."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
  with TestClient(app) as client:
      response = client.get("/health")

  assert response.status_code == 200
  body = response.json()
  assert body["status"] == "ok"
  assert body["app"] == "nexora-agent-backend"


def test_unknown_route_returns_unified_envelope() -> None:
  with TestClient(app) as client:
      response = client.get("/not-exists")

  assert response.status_code == 404
  body = response.json()
  assert body["code"] == 404
  assert "data" in body