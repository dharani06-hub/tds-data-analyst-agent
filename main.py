from fastapi import FastAPI, UploadFile, File
from typing import List, Dict
import pandas as pd
import io

# Import task processors
from processors.network import process_network_data
from processors.sales import process_sales_data
from processors.weather import process_weather_data
from processors.scraper import scrape_and_summarize
from processors.pdf_parser import parse_pdf_and_ask
from processors.image_ocr import process_image_file
from processors.audio_transcriber import process_audio_file

# Fallback LLM handler
from utils.llm import ask_llm

app = FastAPI(
    title="TDS Data Analyst Agent API",
    description="Single endpoint to handle all TDS Data Analyst tasks.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "TDS Data Analyst Agent API is running"}

@app.post("/api/", response_model=Dict)
async def handle_request(
    questions: UploadFile = File(..., description="Upload questions.txt"),
    files: List[UploadFile] = File(default=[], description="Upload any supporting files (CSV, PDF, image, audio)")
):
    """
    Accepts:
    - questions.txt (always required)
    - Zero or more supporting files
    Returns:
    - JSON array or JSON object, depending on the task
    """

    # Read the questions
    questions_text = (await questions.read()).decode().lower()

    # Helper to find file by extension
    def get_file(*exts):
        for f in files:
            if f.filename.lower().endswith(exts):
                return f
        return None

    # --- CSV-based tasks ---
    csv_file = get_file(".csv")
    if csv_file:
        df = pd.read_csv(io.BytesIO(await csv_file.read()))

        if "edge" in questions_text or "network" in questions_text:
            return process_network_data(df)

        elif "sales" in questions_text:
            return process_sales_data(df)

        elif "temperature" in questions_text or "precipitation" in questions_text or "weather" in questions_text:
            return process_weather_data(df)

    # --- Wikipedia scraping ---
    if "wikipedia.org" in questions_text:
        return scrape_and_summarize(questions_text)

    # --- PDF parsing ---
    pdf_file = get_file(".pdf")
    if pdf_file:
        return parse_pdf_and_ask(await pdf_file.read())

    # --- Image OCR ---
    image_file = get_file(".png", ".jpg", ".jpeg")
    if image_file:
        return process_image_file(await image_file.read())

    # --- Audio transcription ---
    audio_file = get_file(".mp3", ".wav")
    if audio_file:
        return process_audio_file(await audio_file.read())

    # --- Fallback to LLM ---
    return {"response": ask_llm(questions_text)}
