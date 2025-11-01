# app/scraper_helpers.py
import os
import json
from pathlib import Path
from typing import List, Tuple

OUTPUT_DIR = "scraped_links"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _state_file(query: str) -> Path:
    safe = query.strip().replace(" ", "_").replace("/", "_").replace(":", "_")
    return Path(OUTPUT_DIR) / f"{safe}_RAW.json"


def load_state(query: str) -> Tuple[List[str], int]:
    """
    Load previous scrape state.
    Returns (list_of_hrefs, last_page_scraped).
    """
    path = _state_file(query)
    if not path.exists():
        return [], 0

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Warning: Failed to read state file ({e}); starting fresh.")
        return [], 0

    hrefs = data.get("hrefs", [])
    last_page = data.get("last_page", 0)
    return hrefs, last_page


def save_state(query: str, hrefs: List[str], last_page: int) -> None:
    """
    Persist the current scrape state 
    """
    path = _state_file(query)
    payload = {
        "hrefs": sorted(hrefs),
        "last_page": last_page,
        "total_unique": len(hrefs),
        "query": query,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"State saved → {path.name} (page {last_page+1}, {len(hrefs)} unique hrefs)")