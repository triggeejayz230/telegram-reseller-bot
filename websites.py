import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def get_footlocker_products():
    base_url = "https://www.footlocker.com.au"
    product_links = []

    for page in range(1, 4):  # Scrape first 3 pages
        url = f"{base_url}/en/c/men/shoes/sneakers?currentPage={page}"
        print(f"🌐 Loading Footlocker page {page}: {url}")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.select("a.ProductCard__Link"):  # Adjusted selector
                href = a.get("href")
                if href and "/en/product/" in href:
                    full_url = base_url + href
                    product_links.append(full_url)

            print(f"   ✅ Page {page}: Found {len(product_links)} links")

        except Exception as e:
            print(f"   ❌ Error on page {page}: {e}")

    return list(set(product_links))  # Remove duplicates
