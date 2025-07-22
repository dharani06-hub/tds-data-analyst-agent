from fastapi import FastAPI, Query
from analyzer.film_scraper import scrape_film_data
from analyzer.court_parser import parse_court_data
from response_generator import generate_response

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TDS Data Analyst Agent is live!"}

@app.get("/analyze")
def analyze(source: str = Query(..., description="Choose source: 'film' or 'court'")):
    if source == "film":
        data = scrape_film_data()
    elif source == "court":
        data = parse_court_data()
    else:
        return {"error": "Invalid source"}
    
    return generate_response(data)
