import pytest
from fastapi.testclient import TestClient
from pdf service.main import app

client = TestClient(app)

def test_upload_pdf():
    with open("sample.pdf", "rb") as f:
        response = client.post("/pdf/upload", files={"file": f})
    assert response.status_code == 200
    data = response.json()
    assert "doc_id" in data
