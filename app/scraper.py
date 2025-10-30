from fastapi import Response
from camoufox.async_api import AsyncCamoufox


async def scrape_url(url: str) -> Response:
    try:
        async with AsyncCamoufox(os="linux", headless=True) as browser:
            page = await browser.new_page()
            await page.goto(url, timeout=100000, wait_until="networkidle")

            html = await page.content()
            cookies = await page.context.cookies()

        response = Response(content=html, media_type="text/html")

        for cookie in cookies:
            response.headers.append(
                "Set-Cookie",
                f"{cookie['name']}={cookie['value']}; Path=/; HttpOnly"
            )

        return response

    except Exception as e:
        raise Exception(f"Scraping failed: {e}")
