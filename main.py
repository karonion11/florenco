import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from subscribers import toggle_subscription
from scheduler import start_scheduler

BOT_TOKEN = "7764442498:AAEVAzBzM8xsBDEDeHMiUUDs-tdyt5NBFAk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(types.KeyboardButton("📦 Заказы без ТТН"))

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=menu)

@dp.message_handler(lambda m: m.text == "📦 Заказы без ТТН")
async def toggle_sub(message: types.Message):
    subscribed = toggle_subscription(message.from_user.id)
    if subscribed:
        await message.answer("✅ Вы подписаны")
    else:
        await message.answer("❌ Вы отписаны")

async def on_startup(dp: Dispatcher):
    start_scheduler(bot)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
