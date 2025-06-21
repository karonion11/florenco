import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.markdown import hbold

from subscribers import toggle_subscription
from scheduler import start_scheduler
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Клавиатура
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Заказы без ТТН")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu)

@dp.message(F.text == "📦 Заказы без ТТН")
async def toggle_sub(message: types.Message):
    subscribed = toggle_subscription(message.from_user.id)
    if subscribed:
        await message.answer("✅ Вы подписаны")
    else:
        await message.answer("❌ Вы отписаны")

async def main():
    start_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
