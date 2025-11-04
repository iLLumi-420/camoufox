from fastapi import FastAPI, Query, HTTPException
from contextlib import asynccontextmanager
from app.scraper import scrape_url, scrape_links_via_api
from browserforge.fingerprints import FingerprintGenerator
from camoufox.async_api import AsyncCamoufox

fg = FingerprintGenerator(browser='firefox')

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context to start/stop a persistent browser.
    """

    config = { 
        'navigator.userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'navigator.platform': 'Win32',
    }

    app.state.browser = await AsyncCamoufox(
        headless=True, 
        os='windows',   
        humanize=True, 
        geoip=False,
        args=['--user-data-dir', 'user-data-dir'], 
        config=config,  # Overrides (optional)
        i_know_what_im_doing=True, 
    ).__aenter__()

    yield
    await app.state.browser.__aexit__(None, None, None)

app = FastAPI(lifespan=lifespan, title="Concurrent Scraper API")



@app.get("/scrape")
async def scrape_endpoint(url: str = Query(..., description="URL to scrape")):
    """
    Scrape a single URL using persistent browser.
    """
    try:
        return await scrape_url(url, app.state.browser)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/links")
async def links_endpoint(query: str = Query(..., description="URL to extract links from")):
    try:
        links = await scrape_links_via_api(query, app.state.browser)
        return {"links_count": len(links), "links": links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
