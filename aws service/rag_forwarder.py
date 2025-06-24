import aiohttp
import asyncio

RAG_INDEX_URL = "http://localhost:8001/rag/index"
RAG_QUERY_URL = "http://localhost:8001/rag/query"

async def post_json(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

def forward_to_rag_index(doc_id: str):
    payload = {"doc_id": doc_id}
    return asyncio.run(post_json(RAG_INDEX_URL, payload))

def forward_to_rag_query(query: dict):
    return asyncio.run(post_json(RAG_QUERY_URL, query))
