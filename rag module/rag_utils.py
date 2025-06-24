import os
import uuid
import time
import openai
import boto3
from typing import List
from pinecone import Pinecone, ServerlessSpec

# Set keys (can also use .env with dotenv)
openai.api_key = "YOUR_OPENAI_API_KEY"
PINECONE_API_KEY = "YOUR_PINECONE_API_KEY"
PINECONE_INDEX_NAME = "your-index-name"
PINECONE_REGION = "us-west-2"

# Initialize Pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if needed
if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_REGION)
    )

index = pc.Index(PINECONE_INDEX_NAME)

# AWS Lambda
lambda_client = boto3.client("lambda", region_name="your-region")

# Helpers
def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    response = openai.Embedding.create(
        input=chunks,
        model="text-embedding-ada-002"
    )
    return [item["embedding"] for item in response["data"]]

def index_document(doc_id: str, text: str):
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    vectors = [{
        "id": f"{doc_id}-{i}",
        "values": embeddings[i],
        "metadata": {"text": chunks[i], "doc_id": doc_id}
    } for i in range(len(chunks))]
    index.upsert(vectors)

def query_document(query: str):
    run_id = str(uuid.uuid4())
    start = time.time()

    query_embedding = openai.Embedding.create(
        input=[query],
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]

    results = index.query(vector=query_embedding, top_k=5, include_metadata=True)
    contexts = [match['metadata']['text'] for match in results['matches']]
    prompt = f"Answer the question using the context:\n\n{''.join(contexts)}\n\nQuestion: {query}\nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    end = time.time()
    answer = response['choices'][0]['message']['content']
    usage = response['usage']

    metrics = {
        "run_id": run_id,
        "answer": answer,
        "tokens_consumed": usage['prompt_tokens'],
        "tokens_generated": usage['completion_tokens'],
        "response_time_ms": int((end - start) * 1000),
        "confidence_score": results['matches'][0]['score'] if results['matches'] else 0
    }

    lambda_client.invoke(
        FunctionName='your-lambda-function-name',
        InvocationType='Event',
        Payload=str(metrics).encode()
    )

    return metrics
