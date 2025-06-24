import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "your-s3-bucket-name"

def upload_to_s3(file_content, filename):
    s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=file_content)

def delete_from_s3(key: str):
    s3.delete_object(Bucket=BUCKET_NAME, Key=key)
