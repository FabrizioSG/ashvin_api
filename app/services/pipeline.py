from pathlib import Path
from sqlalchemy.orm import Session
from .doc_text import extract_text_with_ocr_fallback
from .classifier import classify_text
from .. import crud
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_text(text: str, category: str) -> str:
    """
    Uses OpenAI to generate an analysis/summary of the document.
    """
    system = "You are a helpful assistant that extracts structured information from documents."
    user = f"Document category: {category}\n\nDocument text:\n{text[:8000]}"

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )

    return resp.output_text.strip()

def summarize_text(text: str, category: str) -> str:
    """
    Short summary (1–2 paragraphs) of the whole document.
    """
    system = "You are a helpful assistant that writes short summaries of documents."
    user = f"Summarize this {category} in a concise way (3-5 sentences max):\n\n{text[:6000]}"

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return resp.output_text.strip()

def process_pdf(pdf_path: str, db: Session):
    # 1. Extract text
    text, _ = extract_text_with_ocr_fallback(pdf_path)

    # 2. Classify
    category = classify_text(text if text else "EMPTY")

    # 3. Analyze with OpenAI
    analysis = analyze_text(text, category)

    # 4. Generate a small summary
    summary = summarize_text(text, category)

    # 5. Save to DB
    return crud.save_document(
        db=db,
        file_name=Path(pdf_path).name,
        category=category,
        extracted_text=text,
        analysis=analysis,
        summary=summary,
    )
