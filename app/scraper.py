from camoufox.async_api import AsyncCamoufox
from fastapi import Response

async def scrape_url(url: str, browser: AsyncCamoufox) -> Response:
    try:
        page = await browser.new_page(ignore_https_errors=True)

        await page.goto(url, timeout=30000, wait_until="domcontentloaded")

        await page.wait_for_timeout(2000) 

        html = await page.content()

        cookies = await page.context.cookies()

        await page.close()

        response = Response(content=html, media_type="text/html")
        for cookie in cookies:
            response.headers.append(
                "Set-Cookie",
                f"{cookie['name']}={cookie['value']};"
            )

        return response

    except Exception as e:
        raise Exception(f"Scraping failed: {e}")
