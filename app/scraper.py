import asyncio
import random
import urllib.parse
from typing import List, Set, Dict
from camoufox.async_api import AsyncCamoufox
from fastapi import Response
from app.helpers import load_state, save_state
import httpx
from bs4 import BeautifulSoup





async def scrape_links_via_api(
    query: str,
    broswer: AsyncCamoufox,
    max_pages: int = 35
) -> List[str]:
    existing_hrefs, last_page = load_state(query)
    all_hrefs: Set[str] = set(existing_hrefs)

    if last_page >= max_pages:
        print(f"Already scraped {last_page} page(s) (>= {max_pages}); returning {len(all_hrefs)} stored hrefs.")
        return sorted(all_hrefs)

    encoded_query = urllib.parse.quote(query)


    for page_num in range(last_page, max_pages):
        start = page_num * 10
        google_url = f"https://www.google.com/search?q={encoded_query}&start={start}"
        print(f"Scraping page {page_num + 1}/{max_pages} → {google_url}")

        resp = await scrape_url(google_url, broswer)
        html = resp.body.decode('utf-8')

        hrefs = extract_links_from_html(html)

        old = len(all_hrefs)
        all_hrefs.update(hrefs)  
        print(f"   → {len(hrefs)} hrefs on page, {len(all_hrefs) - old} new unique")

        save_state(query, list(all_hrefs), page_num)

        await asyncio.sleep(random.uniform(1.0, 2.5))


    save_state(query, list(all_hrefs), max_pages - 1)
    return sorted(all_hrefs)
    

def extract_links_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    results: List[str] = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if not href.startswith("http"):
            continue
        if "google.com" in href or "/ads?" in href:
            continue

        if href not in results:
            results.append(href)

    return results

async def scrape_url(url: str, browser: AsyncCamoufox) -> Response:
    """
    Scrape a single page with JS rendered content.
    Returns HTML with cookies in headers.
    """
    try:
        page = await browser.new_page()

        response = await page.goto(url, timeout=120000, wait_until="domcontentloaded")

        if not response or response.status != 200:
            status = response.status if response else "No Response"
            raise Exception(f"Non-200 status: {status}")

        await page.wait_for_timeout(2000)  

        html = await page.content()
        cookies = await page.context.cookies()
        await page.close()

        html_response = Response(content=html, media_type="text/html")
        for cookie in cookies:
            html_response.headers.append(
                "Set-Cookie",
                f"{cookie['name']}={cookie['value']};"
            )
        return html_response

    except Exception as e:
        raise Exception(f"Scraping failed: {e}")