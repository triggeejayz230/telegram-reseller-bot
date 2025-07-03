import time
import requests
import re
from bs4 import BeautifulSoup
from keywords import keywords  # You must have this keywords.py file
from urllib.parse import urljoin

# === Telegram Bot Info ===
BOT_TOKEN = "8175144603:AAG5Zaeu4cdqyMhMZl0aBuoPWQGRjQkwEo8"
CHAT_ID = "6321858073"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def is_keyword_match(product_name):
    name_lower = product_name.lower()
    return any(keyword.lower() in name_lower for keyword in keywords)

def get_ebay_price(product_name):
    # Clean and simplify the search query
    cleaned = re.sub(r'\b(men|women|kids|size\s*\d+|\d+)\b', '', product_name, flags=re.IGNORECASE)
    cleaned = re.sub(r'[^a-zA-Z0-9 ]', '', cleaned)
    cleaned = " ".join(cleaned.split()[:6])  # Use top 6 words

    print(f"🔍 Searching eBay for: {cleaned}")
    url = f"https://www.ebay.com/sch/i.html?_nkw={'+'.join(cleaned.split())}&LH_Sold=1&LH_Complete=1"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        prices = []
        for item in soup.select(".s-item__price"):
            text = item.get_text(strip=True).replace(',', '')
            match = re.search(r'\$([\d\.]+)', text)
            if match:
                prices.append(float(match.group(1)))

        if prices:
            avg_price = round(sum(prices) / len(prices), 2)
            return f"${avg_price} (avg from {len(prices)} items)"
        else:
            return "No sold data"

    except Exception as e:
        print("❌ eBay error:", e)
        return "eBay error"

def scrape_footlocker():
    print("🔄 Checking Footlocker products...")
    base_url = "https://www.footlocker.com.au"
    headers = {"User-Agent": "Mozilla/5.0"}
    all_links = []

    for page in range(1, 4):
        url = f"{base_url}/en/c/men/shoes/sneakers?currentPage={page}"
        print(f"🌐 Loading Footlocker page {page}: {url}")
        try:
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, "html.parser")
            products = soup.select("a.ProductCard-link")
            links = [urljoin(base_url, a.get("href")) for a in products if a.get("href")]
            print(f"   ✅ Page {page}: Found {len(links)} links")
            all_links.extend(links)
        except Exception as e:
            print(f"   ❌ Error on page {page}: {e}")

    print(f"   ✅ Found {len(all_links)} products")

    for product_url in set(all_links):
        try:
            resp = requests.get(product_url, headers=headers)
            soup = BeautifulSoup(resp.text, "html.parser")

            name_tag = soup.select_one("title")
            name = name_tag.get_text(strip=True).split("|")[0] if name_tag else "Name not found"

            price_tag = soup.select_one(".ProductPrice span")
            price = price_tag.get_text(strip=True) if price_tag else "Price not found"

            if is_keyword_match(name):
                ebay_price = get_ebay_price(name)
                message = f"""
🔔 <b>Product Found</b>
🛍️ <b>{name}</b>
💰 <b>{price}</b>
💸 <b>eBay Price:</b> {ebay_price}
🔗 <a href="{product_url}">View Product</a>
"""
                send_telegram_alert(message)
                print("✅ MATCHED:", name)
            else:
                print("❌ Skipped (No match):", name)

        except Exception as e:
            print(f"⚠️ Error scraping product: {e}")

# === Run every 10 minutes
while True:
    scrape_footlocker()
    print("😴 Sleeping for 10 minutes...\n")
    time.sleep(600)
