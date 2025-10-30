from fastapi import FastAPI, Query, HTTPException
from contextlib import asynccontextmanager
from camoufox.async_api import AsyncCamoufox
from app.scraper import scrape_url

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch persistent browser
    app.state.browser = await AsyncCamoufox(os="linux", headless=True).__aenter__()
    yield
    # Shutdown: close browser
    await app.state.browser.__aexit__(None, None, None)

app = FastAPI(lifespan=lifespan)

@app.get("/scrape")
async def scrape_endpoint(url: str = Query(..., description="URL to scrape")):
    try:
        browser = app.state.browser
        return await scrape_url(url, browser)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
