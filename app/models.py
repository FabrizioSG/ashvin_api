from sqlalchemy import Column, Integer, String, Text
from .database import Base

class PDFResult(Base):
    __tablename__ = "pdf_results"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    page_number = Column(Integer)
    analysis_summary = Column(Text)
