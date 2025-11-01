# app/scraper.py
import asyncio
import random
import urllib.parse
from typing import List
from camoufox.async_api import AsyncCamoufox

from app.helpers import load_state, save_state


async def scrape_links(
    query: str, browser: AsyncCamoufox, max_pages: int = 5
) -> List[str]:

    existing_hrefs, last_page = load_state(query)
    all_hrefs: set[str] = set(existing_hrefs)

    if last_page >= max_pages:
        print(
            f"Already scraped {last_page} page(s) (>= {max_pages}); "
            f"returning {len(all_hrefs)} stored hrefs."
        )
        return sorted(all_hrefs)

    encoded_query = urllib.parse.quote(query)
    page = await browser.new_page()


    try:
        for page_num in range(last_page, max_pages):
            start = page_num * 10
            url = f"https://www.google.com/search?q={encoded_query}&start={start}"
            print(f"Scraping page {page_num + 1}/{max_pages} → {url}")

            await page.goto(url, timeout=120_000, wait_until="domcontentloaded")
            await page.wait_for_timeout(random.uniform(1_000, 2_500))

            hrefs = await page.evaluate("""
                () => Array.from(document.querySelectorAll('a'))
                       .map(a => a.href)
                       .filter(h => h && h.startsWith('http'))
            """)

            old = len(all_hrefs)
            all_hrefs.update(hrefs)
            print(
                f"   → {len(hrefs)} hrefs on page, "
                f"{len(all_hrefs) - old} new unique"
            )

            save_state(query, list(all_hrefs), page_num)

            await asyncio.sleep(random.uniform(1.0, 2.5))


        save_state(query, list(all_hrefs), max_pages - 1)
        return sorted(all_hrefs)

    finally:
        await page.close()