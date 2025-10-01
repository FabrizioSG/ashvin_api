from pydantic import BaseModel

class PDFResultBase(BaseModel):
    file_name: str
    page_number: int | None = None
    analysis_summary: str | None = None

class PDFResultCreate(PDFResultBase):
    pass

class PDFResult(PDFResultBase):
    id: int

    class Config:
        orm_mode = True
