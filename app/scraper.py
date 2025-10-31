from camoufox.async_api import AsyncCamoufox
from fastapi import Response
import asyncio


from camoufox.async_api import AsyncCamoufox
from fastapi import Response
import json
import os

OUTPUT_DIR = "scraped_links"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def scrape_links(query: str, browser: AsyncCamoufox) -> list:
    try:
        page = await browser.new_page()

        search_url = f"https://www.google.com/search?q={query}"
        await page.goto(search_url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)  # extra wait for JS

        links = await page.evaluate("""
        () => Array.from(document.querySelectorAll('a'))
                  .map(a => a.href)
        """)

        await page.close()

        safe_query = query.replace(" ", "_").replace(":", "_")
        filename = os.path.join(OUTPUT_DIR, f"{safe_query}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(links, f, indent=2, ensure_ascii=False)

        return links

    except Exception as e:
        raise Exception(f"Google search failed: {e}")
    


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


        await page.wait_for_timeout(5000)  # 2s for JS to finish


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


