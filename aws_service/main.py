from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid

from dynamodb_utils import add_metadata, get_metadata, update_metadata, delete_metadata
from s3_utils import upload_to_s3, delete_from_s3
from rag_forwarder import forward_to_rag_index, forward_to_rag_query

app = FastAPI()

class Metadata(BaseModel):
    title: str
    description: str
    s3_key: str

@app.post("/aws/documents")
async def create_metadata(metadata: Metadata):
    doc_id = str(uuid.uuid4())
    item = {
        "doc_id": doc_id,
        "title": metadata.title,
        "description": metadata.description,
        "s3_key": metadata.s3_key
    }
    add_metadata(item)
    return {"message": "Document metadata added", "doc_id": doc_id}

@app.get("/aws/documents/{doc_id}")
async def read_metadata(doc_id: str):
    item = get_metadata(doc_id)
    if not item:
        raise HTTPException(status_code=404, detail="Document not found")
    return item

@app.put("/aws/documents/{doc_id}")
async def update_document(doc_id: str, metadata: Metadata):
    update_metadata(doc_id, metadata.dict())
    return {"message": "Document metadata updated"}

@app.delete("/aws/documents/{doc_id}")
async def delete_document(doc_id: str, delete_s3: bool = False):
    if delete_s3:
        item = get_metadata(doc_id)
        if item:
            delete_from_s3(item["s3_key"])
    delete_metadata(doc_id)
    return {"message": "Document deleted"}

@app.post("/aws/documents/{doc_id}/index")
async def index_to_rag(doc_id: str):
    response = forward_to_rag_index(doc_id)
    return JSONResponse(content=response)

@app.post("/aws/query")
async def query_to_rag(query: dict):
    response = forward_to_rag_query(query)
    return JSONResponse(content=response)
