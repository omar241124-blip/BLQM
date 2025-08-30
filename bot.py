import os
import time
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Telegram setup ---
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
bot = telebot.TeleBot(BOT_TOKEN)

def send_to_telegram(file_path, caption=""):
    with open(file_path, "rb") as f:
        bot.send_photo(CHAT_ID, f, caption=caption)

# --- Selenium setup ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome without GUI
options.add_argument("--no-sandbox")  # Required for Linux
options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")  # Full-size screenshot

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

driver.get("https://www.coinglass.com/pro/futures/LiquidationMap")
time.sleep(3)
driver.execute_script("window.scrollBy(0, 300);")
time.sleep(2)

# --- Main loop ---
while True:
    try:
        # --- 1 day screenshot ---
        filename_day1 = "1_day.png"
        driver.save_screenshot(filename_day1)
        send_to_telegram(filename_day1, "Liquidation Map - 1 day")
        print("✅ Captured 1 day")

        # --- Click 1 day button to open dropdown ---
        button_1day = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'MuiSelect-button') and contains(., '1 day')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", button_1day)
        driver.execute_script("arguments[0].click();", button_1day)
        time.sleep(1)

        # --- 7 day screenshot ---
        button_7days = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(text(),'7 day')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", button_7days)
        driver.execute_script("arguments[0].click();", button_7days)
        time.sleep(5)

        filename_7days = "7_days.png"
        driver.save_screenshot(filename_7days)
        send_to_telegram(filename_7days, "Liquidation Map - 7 days")
        print("✅ Captured 7 days")

        # --- Switch back to 1 day for next iteration ---
        driver.execute_script("arguments[0].click();", button_7days)  # open dropdown
        time.sleep(1)
        driver.execute_script("arguments[0].click();", button_1day)    # select 1 day
        time.sleep(2)

    except Exception as e:
        print(f"❌ Error during capture: {e}")

    print("⏱ Waiting 1 minute before next capture...")
    time.sleep(60)
