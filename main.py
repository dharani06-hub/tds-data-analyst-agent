from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd
from io import BytesIO
from utils import image_to_text, audio_to_text, ask_llm
from analyzer.film_scraper import scrape_and_summarize
from analyzer.court_parser import parse_pdf_and_ask

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TDS Data Analyst Agent API"}

# 1. Scrape Website
@app.post("/scrape")
def scrape(url: str = Form(...)):
    return scrape_and_summarize(url)

# 2. PDF Parsing
@app.post("/pdf")
async def parse_pdf(file: UploadFile = File(...)):
    content = await file.read()
    return parse_pdf_and_ask(content)

# 3. Image Processing
@app.post("/image")
async def parse_image(file: UploadFile = File(...)):
    content = await file.read()
    return {"response": ask_llm(image_to_text(content))}

# 4. Audio Processing
@app.post("/audio")
async def parse_audio(file: UploadFile = File(...)):
    content = await file.read()
    return {"response": ask_llm(audio_to_text(content))}

# 5. Generic LLM Query
@app.post("/ask")
def ask(query: str = Form(...)):
    return {"response": ask_llm(query)}

# ---- DATASET PROCESSING ----

def process_csv(file: UploadFile):
    """Reads CSV file into pandas DataFrame and returns basic info."""
    content = file.file.read()
    df = pd.read_csv(BytesIO(content))
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "head": df.head(5).to_dict(orient="records")
    }

@app.post("/network")
async def network_data(file: UploadFile = File(...)):
    return process_csv(file)

@app.post("/sales")
async def sales_data(file: UploadFile = File(...)):
    return process_csv(file)

@app.post("/weather")
async def weather_data(file: UploadFile = File(...)):
    return process_csv(file)

   
