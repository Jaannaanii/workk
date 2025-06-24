import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from rag module.main import app

client = TestClient(app)

@patch("rag_module.utils.chunk_pdf_text")
@patch("rag_module.utils.send_metrics_to_lambda")
def test_rag_query(mock_lambda, mock_chunk):
    mock_chunk.return_value = ["chunk1", "chunk2"]
    mock_lambda.return_value = True

    payload = {
        "query": "What is this about?",
        "doc_id": "sample-doc-123"
    }

    response = client.post("/rag/query", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()
