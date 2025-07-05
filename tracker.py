import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import quote
from keywords import keywords  # Your keyword list

# === Telegram Info ===
BOT_TOKEN = "8175144603:AAG5Zaeu4cdqyMhMZl0aBuoPWQGRjQkwEo8"
CHAT_ID = "1856328073"

def send_telegram_alert(message):
    try:
        with open('chat_ids.txt', 'r') as file:
            chat_ids = file.read().splitlines()
    except FileNotFoundError:
        chat_ids = []

    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload)

def is_keyword_match(product_name):
    name_lower = product_name.lower()
    return any(keyword.lower() in name_lower for keyword in keywords)

def get_ebay_price(product_name):
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={quote(product_name)}&LH_Sold=1&LH_Complete=1"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        prices = []
        for item in soup.select(".s-item"):
            price_tag = item.select_one(".s-item__price")
            if price_tag:
                text = price_tag.get_text(strip=True).replace("AU ", "").replace("$", "").replace(",", "")
                try:
                    price = float(text.split(" ")[0])
                    prices.append(price)
                except:
                    continue

        if prices:
            avg_price = sum(prices) / len(prices)
            return f"${avg_price:.2f}"
        else:
            return "No sold data"
    except Exception as e:
        return "eBay Error"

def scrape_footlocker(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        name_tag = soup.select_one('h1')
        name = name_tag.get_text(strip=True) if name_tag else "Name not found"

        price_tag = soup.select_one('.ProductPrice span')
        price = price_tag.get_text(strip=True) if price_tag else "Price not found"

        if is_keyword_match(name):
            ebay_price = get_ebay_price(name)
            message = f"""
🔔 <b>Product Found</b>
🛍️ <b>{name}</b>
💰 <b>{price}</b>
📊 <b>eBay Avg Sold:</b> {ebay_price}
🔗 <a href="{url}">View Product</a>
"""
            send_telegram_alert(message)
            print("✅ MATCHED:", name)
        else:
            print("❌ Skipped (No match):", name)
    except Exception as e:
        print("❌ Error scraping Footlocker:", e)

# === List of products to check
product_urls = [
    "https://www.footlocker.com.au/en/product/nike-air-men-jackets/247450196800.html",
    "https://www.footlocker.com.au/en/product/nike-air-varsity-jacket-men/247450134900.html"
    # Add more if you want
]

# === Run forever every 10 minutes
while True:
    print("🔄 Checking Footlocker products...")
    for url in product_urls:
        scrape_footlocker(url)
    print("😴 Sleeping for 10 minutes...\n")
    time.sleep(600)
