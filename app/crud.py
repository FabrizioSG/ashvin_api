from sqlalchemy.orm import Session
from . import models, schemas

def create_result(db: Session, result: schemas.PDFResultCreate):
    db_result = models.PDFResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_results(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PDFResult).offset(skip).limit(limit).all()
