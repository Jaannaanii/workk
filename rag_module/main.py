from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from rag_utils import index_document, query_document

app = FastAPI()

class IndexRequest(BaseModel):
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    query: str

@app.post("/rag/index")
def index_doc(req: IndexRequest):
    try:
        index_document(req.doc_id, req.text)
        return {"status": "indexed", "doc_id": req.doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/query")
def query_doc(req: QueryRequest):
    try:
        return query_document(req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
