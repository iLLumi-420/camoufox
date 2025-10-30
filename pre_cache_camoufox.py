# pre_cache_camoufox.py
import asyncio
from camoufox.async_api import AsyncCamoufox

async def main():
    # Launch Camoufox once to download and cache the binary
    async with AsyncCamoufox(os="linux", headless=True):
        pass

asyncio.run(main())