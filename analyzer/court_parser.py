
import fitz  # PyMuPDF
from utils import ask_llm

def parse_pdf_and_ask(content: bytes):
    doc = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return {"response": ask_llm(f"Analyze this legal document: {text[:3000]}")}

