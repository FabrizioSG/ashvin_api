# 📄 Document Classifier API

This backend is a **FastAPI** application that processes PDF documents, classifies them into 6 categories, extracts text (with OCR fallback), and generates both a **summary** and a detailed **analysis** using OpenAI GPT.  

The results are stored in a **SQLite database** and can be accessed via REST API endpoints.

---

## 🚀 Features

- Upload **one or many PDFs** at once.  
- Auto **OCR fallback** for scanned PDFs.  
- Classifies documents into:
  - Compliance Report  
  - Delivery Ticket  
  - Order  
  - Physician Notes  
  - Prescription  
  - Sleep Study Report  
- Generates:
  - **Summary** (short paragraph)  
  - **Detailed Analysis** (Markdown-rich structured output)  
- Stores results in **SQLite** for later retrieval.  
- REST API built with **FastAPI**.  

---

## 📦 Requirements

- Python **3.11+**
- Tesseract OCR (for scanned PDFs)  
  - Install on macOS: `brew install tesseract`  
  - Install on Ubuntu/Debian: `sudo apt install tesseract-ocr`  

### Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
### Install requirements
pip install -r requirements.txt

### Run the app
uvicorn app.main:app --reload



