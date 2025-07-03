import requests
from bs4 import BeautifulSoup

def get_average_ebay_price(product_name):
    query = product_name.replace(" ", "+")
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&LH_Sold=1&LH_Complete=1"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")

        prices = []
        for item in soup.select(".s-item"):
            price_tag = item.select_one(".s-item__price")
            if price_tag:
                price_text = price_tag.get_text().replace("$", "").replace(",", "")
                try:
                    price = float(price_text.split()[0])
                    prices.append(price)
                except:
                    continue

        if prices:
            avg_price = round(sum(prices) / len(prices), 2)
            return avg_price, url
        else:
            return None, url
    except Exception as e:
        print("❌ eBay Error:", e)
        return None, url
