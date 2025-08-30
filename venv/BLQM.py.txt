import asyncio
from playwright.async_api import async_playwright
from telegram import Bot
import time

TOKEN = "8242720791:AAGnYu4Sp1hQCJPIBcr1bGWJTcnk7KJX6lo"
CHAT_ID = "1144838994E"

URL = "https://coinglass.com/LiquidationMap"

async def take_screenshot(day, filename):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(URL)

        # Click the dropdown and select the day range
        await page.click('text=7 day')  # dropdown
        await page.click(f'text={day} day')  # 1 / 7 / 30

        await page.screenshot(path=filename, full_page=True)
        await browser.close()

async def main():
    bot = Bot(token=TOKEN)
    while True:
        for day in [1, 7, 30]:
            filename = f"liquidation_{day}d.png"
            await take_screenshot(day, filename)
            await bot.send_photo(chat_id=CHAT_ID, photo=open(filename, "rb"))
        time.sleep(60)  # wait 1 minute

if __name__ == "__main__":
    asyncio.run(main())
