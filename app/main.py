from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path

from . import models, schemas, crud, database
from .services.pipeline import process_pdf
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

# DB setup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Document Classifier API")

# ✅ Allow frontend origin (React runs on http://localhost:3000 by default)
origins = [
    "http://localhost:3000",   # React dev server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # allow specific origins
    allow_credentials=True,
    allow_methods=["*"],            # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # allow all headers
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Health check with OpenAI call
@app.get("/health")
def health_check():
    try:
        client = OpenAI(api_key="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")
        resp = client.responses.create(
            model="gpt-4o-mini",
            input="Reply with 'pong' if you are alive."
        )
        return {
            "status": "ok",
            "openai_response": resp.output_text
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }
# ✅ Upload + classify + analyze
@app.post("/classify/upload", response_model=schemas.Document)
async def classify_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    tmp_dir = Path("uploads")
    tmp_dir.mkdir(exist_ok=True)
    file_path = tmp_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return process_pdf(str(file_path), db=db)

# ✅ List stored documents
@app.get("/documents/", response_model=list[schemas.Document])
def list_docs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.list_documents(db, skip=skip, limit=limit)

# ✅ Get one document
@app.get("/documents/{doc_id}", response_model=schemas.Document)
def get_doc(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


