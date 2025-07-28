from fastapi import FastAPI, UploadFile, File, Form
from analyzer.film_scraper import scrape_and_summarize
from analyzer.court_parser import parse_pdf_and_ask
from utils import image_to_text, audio_to_text, ask_llm

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TDS Data Analyst Agent API"}

@app.post("/scrape")
def scrape(url: str = Form(...)):
    return scrape_and_summarize(url)

@app.post("/pdf")
async def parse_pdf(file: UploadFile = File(...)):
    content = await file.read()
    return parse_pdf_and_ask(content)

@app.post("/image")
async def parse_image(file: UploadFile = File(...)):
    content = await file.read()
    return {"response": ask_llm(image_to_text(content))}

@app.post("/audio")
async def parse_audio(file: UploadFile = File(...)):
    content = await file.read()
    return {"response": ask_llm(audio_to_text(content))}

@app.post("/ask")
def ask(query: str = Form(...)):
    return {"response": ask_llm(query)}
