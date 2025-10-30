from fastapi import FastAPI, Query
from app.scraper import scrape_url  # import your async scraper function

app = FastAPI(
    title="Scraper API",
    description="Scrapes a page using Camoufox and returns HTML with cookies in the header.",
    version="1.0.0",
)

@app.get("/scrape")
async def scrape_endpoint(url: str = Query(..., description="URL to scrape")):
    # since scrape_url is async, we must await it
    return await scrape_url(url)
