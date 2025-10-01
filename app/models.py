from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    extracted_text = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)  # OpenAI-generated analysis
    summary = Column(Text, nullable=True)


