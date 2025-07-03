from telegram.ext import Updater, CommandHandler
import logging
import requests
from bs4 import BeautifulSoup

# === SETUP LOGGING ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === YOUR BOT TOKEN ===
TOKEN = '8175144603:AAG5Zaeu4cdqyMhMZl0aBuoPWQGRjQkwEo8'

# === PRODUCT LINKS TO SCRAPE ===
product_urls = [
    "https://www.footlocker.com.au/en/product/~/244105467104.html",

    # Add more product links here
]

# === SCRAPE FUNCTION ===
def scrape_product(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        name_tag = soup.select_one("h1")
        name = name_tag.get_text(strip=True) if name_tag else "Name not found"

        price_tag = soup.select_one(".product-price, .price, .ProductPrice")
        price = price_tag.get_text(strip=True) if price_tag else "Price not found"

        return f"✅ Product: {name}\n💰 Price: {price}\n🔗 Link: {url}"

    except Exception as e:
        return f"❌ Failed to scrape {url}:\n{str(e)}"


# === COMMANDS ===
def start(update, context):
    update.message.reply_text("👋 Welcome! I'm your product tracking bot.")

def help_command(update, context):
    update.message.reply_text("📋 Available commands:\n/start\n/help\n/ping\n/check")

def ping(update, context):
    update.message.reply_text("🏓 Pong!")

def check(update, context):
    update.message.reply_text("🔍 Checking products...")
    for url in product_urls:
        result = scrape_product(url)
        update.message.reply_text(result)
    update.message.reply_text("✅ Done checking.")

# === MAIN FUNCTION ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("check", check))

    updater.start_polling()
    print("🤖 Bot is listening for commands...")
    updater.idle()

# === RUN THE BOT ===
if __name__ == '__main__':
    main()
