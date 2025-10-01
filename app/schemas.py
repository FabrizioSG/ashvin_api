from pydantic import BaseModel
from typing import Literal, Optional

# Fixed categories
Category = Literal[
    "compliance_report",
    "delivery_ticket",
    "order",
    "physician_notes",
    "prescription",
    "sleep_study_report",
    "unknown"
]


class DocumentBase(BaseModel):
    file_name: str
    category: Category
    extracted_text: str
    analysis: Optional[str] = None  # OpenAI analysis (JSON-like or plain text)
    summary: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    class Config:
        from_attributes = True

