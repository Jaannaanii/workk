import pytest
from unittest.mock import patch
from lambda.store_agent_metrics import lambda_handler

@patch("boto3.client")
def test_lambda_handler(mock_boto):
    event = {
        "run_id": "abc123",
        "timestamp": "2025-01-01T00:00:00Z",
        "agent_name": "AgentX",
        "tokens": 120,
        "response_time": 0.34,
        "confidence": 0.88,
        "status": "success"
    }
    context = {}

    mock_client = mock_boto.return_value
    mock_client.put_item.return_value = {}

    result = lambda_handler(event, context)
    assert result["statusCode"] == 200
