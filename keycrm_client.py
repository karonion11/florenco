import aiohttp
from typing import List, Dict

KEYCRM_TOKEN = "MzkzMzBlNjNjZTUyNTc2ZGUwYTExOTU4NzUyNzJiMGNhNzY2M2ZhNQ"
BASE_URL = "https://api.keycrm.app/v1"

async def fetch_orders_without_ttn() -> List[Dict]:
    headers = {"Authorization": f"Bearer {KEYCRM_TOKEN}"}
    params = {"status": "new,in_work,confirmed"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/orders", headers=headers, params=params) as resp:
            data = await resp.json()
    orders = data.get("data", data)
    result = []
    for order in orders:
        ttn = order.get("ttn") or order.get("delivery_tracking_number")
        if not ttn:
            result.append({
                "id": order.get("id"),
                "status": order.get("status") or order.get("status_name", "")
            })
    return result
