import requests
import time

BASE_URL = "http://localhost:8000/scrape"

urls = [
    "https://www.daraz.com.np",
    "https://www.khalti.com",
    "https://www.esewa.com.np",
    "https://www.hamrobazar.com",
    "https://www.onlinekhabar.com",
    "https://www.setopati.com",
    "https://thehimalayantimes.com",
    "https://myrepublica.nagariknetwork.com",
    "https://kathmandupost.com",
    "https://www.annapurnapost.com",
    "https://bizmandu.com",
    "https://ekantipur.com",
    "https://nepalipatra.com",
    "https://ratopati.com",
    "https://www.nepalminute.com",
    "https://www.newsofnepal.com",
    "https://www.nepalitimes.com",
    "https://nayapatrikadaily.com",
    "https://www.sharesansar.com",
    "https://merolagani.com",
    "https://www.nepalstock.com",
    "https://www.jobsnepal.com",
    "https://merojob.com",
    "https://kantipurjob.com",
    "https://www.collegenp.com",
    "https://www.edusanjal.com",
    "https://www.gariwala.com.np",
    "https://www.nlocarhub.com",
    "https://nepbay.com",
    "https://www.kirana.com.np",
    "https://www.foodmandu.com",
    "https://www.bhojdeals.com",
    "https://www.pathao.com/np",
    "https://tootle.today",
    "https://www.ridegreen.com.np",
    "https://www.nepalairlines.com.np",
    "https://www.buddhaair.com",
    "https://www.yetiairlines.com",
    "https://www.nepaltelecom.com.np",
    "https://www.ncell.axiata.com",
    "https://www.nicasiabank.com",
    "https://www.globalimebank.com",
    "https://www.nabilbank.com",
    "https://www.megabanknepal.com",
    "https://www.prabhubank.com",
    "https://www.nepalbank.com.np",
    "https://www.standardchartered.com/np",
    "https://www.sct.com.np",
    "https://nepalrastriyabank.gov.np",
    "https://www.nepal.gov.np"
]

print(f"{len(urls)} requests...\n")

for i, url in enumerate(urls, start=1):
    full_url = f"{BASE_URL}?url={url}"
    print(f"[{i}] Fetching: {url}")
    start = time.time()
    try:
        res = requests.get(full_url, timeout=60)
        elapsed = round(time.time() - start, 2)
        print(f" → Status: {res.status_code}, Time: {elapsed}s, HTML length: {len(res.text)}")
    except Exception as e:
        print(f" Error: {e}")
    print("-" * 60)

print("\n Done!")
