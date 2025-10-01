from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "FastAPI with SQLite is running!"}

# ✅ Simple test endpoint
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "FastAPI is connected and working!"}

@app.post("/results/", response_model=schemas.PDFResult)
def create_result(result: schemas.PDFResultCreate, db: Session = Depends(get_db)):
    return crud.create_result(db=db, result=result)

@app.get("/results/", response_model=list[schemas.PDFResult])
def read_results(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_results(db, skip=skip, limit=limit)

