import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

STATE_FILE = "playwright_state.json"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/116.0.0.0 Safari/537.36"
)

load_dotenv()
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")


async def _perform_login(page) -> None:
    await page.goto("https://www.instagram.com/accounts/login/", wait_until="networkidle")
    await page.fill("input[name='username']", IG_USERNAME)
    await page.fill("input[name='password']", IG_PASSWORD)
    await page.click("button[type='submit']")
    await page.wait_for_load_state("networkidle")
    # Dismiss possible dialogs like "Save Your Login Info?" or notifications
    for text in ["Not Now", "Не сейчас", "Save Info", "Сохранить информацию"]:
        try:
            await page.click(f"text={text}", timeout=3000)
        except Exception:
            pass


async def _ensure_context(browser):
    context_args = {"user_agent": USER_AGENT}
    if os.path.exists(STATE_FILE):
        context_args["storage_state"] = STATE_FILE
    context = await browser.new_context(**context_args)
    page = await context.new_page()
    await page.goto("https://www.instagram.com/", wait_until="networkidle")
    if "login" in page.url:
        if not IG_USERNAME or not IG_PASSWORD:
            raise RuntimeError("IG_USERNAME or IG_PASSWORD not set in .env")
        await _perform_login(page)
        await context.storage_state(path=STATE_FILE)
    return context, page


async def _collect_unread(page):
    await page.goto("https://www.instagram.com/direct/inbox/", wait_until="networkidle")
    await page.wait_for_selector("a[href*='/direct/t/']")
    threads = page.locator("a[href*='/direct/t/']")
    unread = []
    count = await threads.count()
    for i in range(count):
        item = threads.nth(i)
        is_unread = False
        if await item.locator("svg[aria-label='Unread']").count() > 0:
            is_unread = True
        elif await item.locator("div[style*='font-weight: 600']").count() > 0:
            is_unread = True
        username = await item.locator("div[dir='auto'] span").first.inner_text()
        last_message = await item.locator("div[dir='auto']").nth(-1).inner_text()
        if is_unread:
            unread.append((username, last_message))
    return unread


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context, page = await _ensure_context(browser)
        unread = await _collect_unread(page)
        print(f"Количество непрочитанных тредов: {len(unread)}")
        for username, text in unread:
            print(f"- {username}: {text}")
        await context.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
