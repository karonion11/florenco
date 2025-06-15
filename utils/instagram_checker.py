import os
import requests
from dotenv import load_dotenv

load_dotenv()

IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def notify_telegram(message: str) -> dict:
    """Send a notification to Telegram."""
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("BOT_TOKEN and CHAT_ID must be set")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    response.raise_for_status()
    return response.json()


def check_instagram() -> list:
    """Check Instagram conversations for unread messages."""
    if not IG_ACCESS_TOKEN:
        raise ValueError("IG_ACCESS_TOKEN must be set")
    url = "https://graph.facebook.com/v19.0/me/conversations"
    params = {
        "platform": "instagram",
        "fields": "unread_count",
        "access_token": IG_ACCESS_TOKEN,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    conversations = data.get("data", [])
    for conv in conversations:
        if conv.get("unread_count", 0) > 0:
            notify_telegram("📩 Есть непрочитанные в Instagram!")
            break
    return conversations
