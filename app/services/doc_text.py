import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io

def extract_text_with_ocr_fallback(pdf_path: str, max_pages: int | None = None, dpi: int = 300):
    """
    Extract text from a PDF:
    1) Try pdfplumber (text-based).
    2) If no text -> OCR with pytesseract.
    """
    text_parts = []

    # Try native text extraction
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages
            if max_pages:
                pages = pages[:max_pages]
            for page in pages:
                t = page.extract_text() or ""
                if t.strip():
                    text_parts.append(t)
        if text_parts:
            return "\n".join(text_parts), False
    except Exception:
        pass

    # OCR fallback
    images = convert_from_path(pdf_path, dpi=dpi)
    if max_pages:
        images = images[:max_pages]

    ocr_parts = []
    for img in images:
        if not isinstance(img, Image.Image):
            img = Image.open(io.BytesIO(img))
        ocr_parts.append(pytesseract.image_to_string(img))

    return "\n".join(ocr_parts).strip(), True
