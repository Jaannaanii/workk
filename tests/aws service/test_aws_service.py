from fastapi.testclient import TestClient
from aws service.main import app

client = TestClient(app)

def test_create_document():
    payload = {"doc_id": "doc123", "title": "Test PDF", "uploaded_at": "2024-01-01T00:00:00"}
    response = client.post("/aws/documents", json=payload)
    assert response.status_code == 200

def test_get_document():
    response = client.get("/aws/documents/doc123")
    assert response.status_code in [200, 404]
