import requests
from bs4 import BeautifulSoup
from utils import ask_llm

def scrape_and_summarize(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Basic text extraction (you can customize further)
    text = soup.get_text()
    return {"response": ask_llm(f"Summarize this webpage: {text[:3000]}")}
