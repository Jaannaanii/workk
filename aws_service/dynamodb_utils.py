import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("DocumentMetadata")

def add_metadata(item: dict):
    table.put_item(Item=item)

def get_metadata(doc_id: str):
    response = table.get_item(Key={"doc_id": doc_id})
    return response.get("Item")

def update_metadata(doc_id: str, metadata: dict):
    update_expr = "SET " + ", ".join(f"{k}=:{k}" for k in metadata)
    expr_attr_values = {f":{k}": v for k, v in metadata.items()}
    table.update_item(
        Key={"doc_id": doc_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_values
    )

def delete_metadata(doc_id: str):
    table.delete_item(Key={"doc_id": doc_id})
