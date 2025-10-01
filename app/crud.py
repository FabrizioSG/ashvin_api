from sqlalchemy.orm import Session
from . import models, schemas

def save_document(
    db: Session,
    file_name: str,
    category: str,
    extracted_text: str,
    analysis: str | None = None,
    summary: str | None = None
):
    doc = models.DocumentRecord(
        file_name=file_name,
        category=category,
        extracted_text=extracted_text,
        analysis=analysis,
        summary=summary

    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_document(db: Session, doc_id: int):
    return db.query(models.DocumentRecord).filter(models.DocumentRecord.id == doc_id).first()

def list_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DocumentRecord).offset(skip).limit(limit).all()

def delete_document(db: Session, doc_id: int):
    doc = get_document(db, doc_id)
    if doc:
        db.delete(doc)
        db.commit()
    return doc


