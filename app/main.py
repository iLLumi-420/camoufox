from fastapi import FastAPI, Query, HTTPException
from contextlib import asynccontextmanager
from app.scraper import scrape_links

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context to start/stop a persistent browser.
    """
    from camoufox.async_api import AsyncCamoufox
    app.state.browser = await AsyncCamoufox(os="linux", headless=True).__aenter__()
    yield
    await app.state.browser.__aexit__(None, None, None)

app = FastAPI(lifespan=lifespan, title="Concurrent Scraper API")

# @app.get("/scrape")
# async def scrape_endpoint(url: str = Query(..., description="URL to scrape")):
#     """
#     Scrape a single URL using persistent browser.
#     """
#     try:
#         return await scrape_url(url, app.state.browser)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/links")
async def links_endpoint(query: str = Query(..., description="URL to extract links from")):
    try:
        links = await scrape_links(query, app.state.browser)
        return {"links_count": len(links), "links": links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
