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
    caption = generate_caption()  # заглушка
    await msg.answer(f"✨ Предложение поста:\n\n{caption}")

if __name__ == "__main__":
    print("🚀 Bot is running...")
    executor.start_polling(dp)
