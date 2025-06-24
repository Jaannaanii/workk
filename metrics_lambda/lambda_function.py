import json
import boto3
import os
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import NoRegionError

# Set your AWS region explicitly
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")  # Change to your region

# Initialize DynamoDB with region
try:
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
except NoRegionError:
    raise Exception("AWS region not specified. Set AWS_REGION env variable or configure AWS CLI.")

# Get table name from environment or use default
table_name = os.environ.get('TABLE_NAME', 'AgentMetrics')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        # Check required fields
        required_fields = ["run_id", "timestamp", "agent_name", "tokens", "response_time", "confidence", "status"]
        for field in required_fields:
            if field not in body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Missing field: {field}"})
                }

        item = {
            "run_id": body["run_id"],
            "timestamp": body["timestamp"],
            "agent_name": body["agent_name"],
            "tokens": int(body["tokens"]),
            "response_time": Decimal(str(body["response_time"])),
            "confidence": Decimal(str(body["confidence"])),
            "status": body["status"]
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Metrics stored successfully."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
