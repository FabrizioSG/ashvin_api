import json
import re
from openai import OpenAI

client = OpenAI(api_key="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")

CATEGORIES = [
    "compliance_report",
    "delivery_ticket",
    "order",
    "physician_notes",
    "prescription",
    "sleep_study_report",
]

def classify_text(text: str) -> str:
    """
    Classify document text into one of 6 categories using OpenAI.
    Returns category only.
    """
    prompt = f"""
    Classify this document into one of:
    {", ".join(CATEGORIES)}.

    Return JSON with exactly this format:
    {{
      "category": "<one of the 6>"
    }}

    Document:
    {text[:2000]}
    """

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )

    raw_output = resp.output_text.strip()
    try:
        cleaned = clean_json(raw_output)
        data = json.loads(cleaned)
        category = data.get("category", "unknown")
    except Exception:
        category = "unknown"

    return category




def clean_json(raw: str) -> str:
    # Remove Markdown fences like ```json ... ``` that were causing issues in .loads
    cleaned = re.sub(r"```[a-zA-Z]*", "", raw)
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()


