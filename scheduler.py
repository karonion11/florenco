import asyncio
from aiogram import Bot

from keycrm_client import fetch_orders_without_ttn
from subscribers import load_subscribers
from utils import is_working_hours

CHECK_INTERVAL = 3 * 60 * 60  # 3 hours

async def _check_and_notify(bot: Bot):
    await asyncio.sleep(10)  # small delay before first run
    while True:
        if is_working_hours():
            orders = await fetch_orders_without_ttn()
            if orders:
                subs = load_subscribers()
                for chat_id in subs:
                    for order in orders:
                        msg = f"⚠️ Заказ #{order['id']} ({order['status']}) без ТТН"
                        await bot.send_message(chat_id, msg)
        await asyncio.sleep(CHECK_INTERVAL)

def start_scheduler(bot: Bot):
    loop = asyncio.get_event_loop()
    loop.create_task(_check_and_notify(bot))
