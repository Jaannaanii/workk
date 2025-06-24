from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from uuid import uuid4
from datetime import datetime
import os
import shutil
from PyPDF2 import PdfReader
from db import metadata_store

app = FastAPI(title="PDF Upload & Extraction API")
UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "PDF API is running!"}

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

@app.post("/pdf/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    response = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        doc_id = str(uuid4())
        saved_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
        
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = extract_text_from_pdf(saved_path)
        timestamp = datetime.now().isoformat()

        metadata_store[doc_id] = {
            "doc_id": doc_id,
            "filename": file.filename,
            "path": saved_path,
            "timestamp": timestamp,
            "text": extracted_text,
        }

        response.append({
            "doc_id": doc_id,
            "filename": file.filename,
            "timestamp": timestamp,
        })
    return response

@app.get("/pdf/documents/{doc_id}")
def get_document(doc_id: str):
    doc = metadata_store.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "doc_id": doc["doc_id"],
        "filename": doc["filename"],
        "timestamp": doc["timestamp"],
        "text": doc["text"],
    }

@app.get("/pdf/documents")
def list_documents(page: int = 1, limit: int = 10):
    items = list(metadata_store.values())
    start = (page - 1) * limit
    end = start + limit
    paginated = items[start:end]
    return {
        "page": page,
        "limit": limit,
        "total": len(items),
        "documents": [
            {
                "doc_id": doc["doc_id"],
                "filename": doc["filename"],
                "timestamp": doc["timestamp"],
            }
            for doc in paginated
        ]
    }
