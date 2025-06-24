import lambda_function

# Simulated event payload
event = {
    "run_id": "test-1234",
    "timestamp": "2025-06-24T14:00:00Z",
    "agent_name": "TestAgent",
    "tokens": 120,
    "response_time": 0.84,
    "confidence": 0.95,
    "status": "success"
}

# Call the handler
response = lambda_function.lambda_handler(event, None)
print(response)
