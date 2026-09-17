import os

# Ensure the OpenAI client can be constructed at import time without a real key.
os.environ.setdefault("OPENAI_API_KEY", "test-key")

from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_version():
    client = app.test_client()
    response = client.get("/version")
    assert response.status_code == 200
    body = response.get_json()
    assert body["name"] == "research-report-generator"
    assert "version" in body


def test_generate_report_requires_topic():
    client = app.test_client()
    response = client.post("/generate_report", json={"topic": ""})
    assert response.status_code == 400


def test_unknown_route_returns_json_404():
    client = app.test_client()
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}
