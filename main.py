import time
from utils.instagram_checker import check_instagram
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import os
from dotenv import load_dotenv
from utils.caption_writer import generate_caption

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(msg: Message):
    caption = generate_caption()
    await msg.answer(f"✨ Предложение поста:\n\n{caption}")
### ah
async def periodic_check():
    while True:
        try:
            check_instagram()
        except Exception as exc:
            print(f"Error during check: {exc}")
        time.sleep(300)

if __name__ == "__main__":
    print("🚀 Bot is running...")
    executor.start_polling(dp)
