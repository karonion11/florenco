import asyncio
from instagram_checker import main as check_unread_messages


async def periodic_check() -> None:
    """Periodically check Instagram for unread messages."""
    while True:
        try:
            await check_unread_messages()
        except Exception as exc:
            print(f"Error during check: {exc}")
        await asyncio.sleep(300)


if __name__ == "__main__":
    print("🚀 Bot is running...")
    try:
        asyncio.run(periodic_check())
    except KeyboardInterrupt:
        pass
