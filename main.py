from fastapi import FastAPI, UploadFile, File
from typing import List
from analyzer.film_scraper import scrape_and_summarize
from analyzer.court_parser import parse_pdf_and_ask
from utils import image_to_text, audio_to_text, ask_llm

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TDS Data Analyst Agent API"}

# ✅ New general POST endpoint
@app.post("/api/")
async def handle_request(
    questions: UploadFile = File(...),
    files: List[UploadFile] = File(default=[])
):
    # Read questions.txt
    questions_text = (await questions.read()).decode()

    # Decide which processing pipeline to call
    result = None
    if "wikipedia.org" in questions_text.lower():
        result = scrape_and_summarize(questions_text)
    elif any(f.filename.lower().endswith(".pdf") for f in files):
        for f in files:
            if f.filename.lower().endswith(".pdf"):
                content = await f.read()
                result = parse_pdf_and_ask(content)
                break
    elif any(f.filename.lower().endswith((".png", ".jpg", ".jpeg")) for f in files):
        for f in files:
            if f.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                content = await f.read()
                result = {"response": ask_llm(image_to_text(content))}
                break
    elif any(f.filename.lower().endswith((".mp3", ".wav")) for f in files):
        for f in files:
            if f.filename.lower().endswith((".mp3", ".wav")):
                content = await f.read()
                result = {"response": ask_llm(audio_to_text(content))}
                break
    else:
        # Default: send directly to LLM
        result = {"response": ask_llm(questions_text)}

    return result
