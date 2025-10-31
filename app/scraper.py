from camoufox.async_api import AsyncCamoufox
from fastapi import Response
import asyncio

async def scrape_url(url: str, browser: AsyncCamoufox) -> Response:
    """
    Scrape a single page with JS rendered content.
    Returns HTML with cookies in headers.
    """
    try:
        page = await browser.new_page()
        # Wait until DOMContentLoaded, then short extra wait
        response = await page.goto(url, timeout=120000, wait_until="domcontentloaded")

        if not response or response.status != 200:
            status = response.status if response else "No Response"
            raise Exception(f"Non-200 status: {status}")


        await page.wait_for_timeout(2000)  # 2s for JS to finish

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


async def scrape_multiple(urls: list, browser: AsyncCamoufox, concurrency: int = 5) -> list:
    """
    Scrape multiple URLs concurrently with a persistent browser.

    Args:
        urls (list): List of URLs
        browser (AsyncCamoufox): Persistent browser instance
        concurrency (int): Number of concurrent pages

    Returns:
        list: List of Responses or Exceptions
    """
    semaphore = asyncio.Semaphore(concurrency)

    async def sem_task(url):
        async with semaphore:
            try:
                return await scrape_url(url, browser)
            except Exception as e:
                return e

    tasks = [sem_task(url) for url in urls]
    return await asyncio.gather(*tasks)
