import asyncio
from instagram_checker import check_unread_messages
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import os
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))


async def periodic_check() -> None:
    """Periodically check Instagram for unread messages."""
    while True:
        try:
            check_unread_messages()
        except Exception as exc:
            print(f"Error during check: {exc}")
        await asyncio.sleep(300)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_check())
    print("🚀 Bot is running...")
