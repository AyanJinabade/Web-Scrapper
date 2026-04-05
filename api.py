from fastapi import FastAPI
from scraper.scraper_bs4 import scrape_multiple_pages
from processing.clean_data import clean_data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Web Scraper API Running"}

@app.get("/scrape")
def scrape():
    data = scrape_multiple_pages()
    df = clean_data(data)

    return df.to_dict(orient="records")