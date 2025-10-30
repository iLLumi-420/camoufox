import requests
import time

BASE_URL = "http://localhost:8000/scrape"

urls = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.youtube.com",
    "https://www.reddit.com",
    "https://www.twitter.com",
    "https://www.facebook.com",
    "https://www.instagram.com",
    "https://www.amazon.com",
    "https://www.apple.com",
    "https://www.microsoft.com",
    "https://www.netflix.com",
    "https://www.spotify.com",
    "https://www.cnn.com",
    "https://www.nytimes.com",
    "https://www.bbc.com",
    "https://www.yahoo.com",
    "https://www.tesla.com",
    "https://www.nike.com",
    "https://www.adobe.com",
    "https://www.salesforce.com",
    "https://www.airbnb.com",
    "https://www.booking.com",
    "https://www.linkedin.com",
    "https://www.dropbox.com",
    "https://www.quora.com",
    "https://www.medium.com",
    "https://www.imdb.com",
    "https://www.pinterest.com",
    "https://www.paypal.com",
    "https://www.shopify.com",
    "https://www.figma.com",
    "https://www.behance.net",
    "https://www.twitch.tv",
    "https://www.discord.com",
    "https://www.slack.com",
    "https://www.canva.com",
    "https://www.udemy.com",
    "https://www.coursera.org",
    "https://www.khanacademy.org",
    "https://www.etsy.com",
    "https://www.stackoverflow.com",
    "https://www.github.com",
    "https://www.digitalocean.com",
    "https://www.cloudflare.com",
    "https://www.oracle.com",
    "https://www.intel.com",
    "https://www.samsung.com",
    "https://www.sony.com",
    "https://www.hp.com",
    "https://www.lenovo.com",
]

print(f"\n Starting {len(urls)} scrape requests...\n")

total_start = time.time()
times = []

for i, url in enumerate(urls, start=1):
    full_url = f"{BASE_URL}?url={url}"
    print(f"[{i:02}] Fetching: {url}")
    start = time.time()
    try:
        res = requests.get(full_url, timeout=90)
        elapsed = round(time.time() - start, 2)
        times.append(elapsed)
        print(f" → Status: {res.status_code}, Time: {elapsed}s, HTML length: {len(res.text)}")
    except Exception as e:
        print(f" ❌ Error: {e}")
    print("-" * 70)

total_elapsed = round(time.time() - total_start, 2)
avg_time = round(sum(times) / len(times), 2) if times else 0

print(f"\nDone! Total time: {total_elapsed}s")
print(f"Average time per request: {avg_time}s\n")
