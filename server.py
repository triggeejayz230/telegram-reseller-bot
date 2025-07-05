from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = '8175144603:AAG5Zaeu4cdqyMhMZl0aBuoPWQGRjQkwEo8'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

CHAT_ID_FILE = 'chat_ids.txt'

def save_chat_id(chat_id):
    try:
        with open(CHAT_ID_FILE, 'r') as file:
            chat_ids = set(file.read().splitlines())
    except FileNotFoundError:
        chat_ids = set()

    if str(chat_id) not in chat_ids:
        with open(CHAT_ID_FILE, 'a') as file:
            file.write(f"{chat_id}\n")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == '/start':
            save_chat_id(chat_id)
            send_message(chat_id, "✅ You’ve subscribed to alerts!")
    return "ok"

def send_message(chat_id, text):
    requests.post(BASE_URL + 'sendMessage', data={'chat_id': chat_id, 'text': text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
