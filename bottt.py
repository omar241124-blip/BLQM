import time
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Telegram setup ---
BOT_TOKEN = "8242720791:AAEtNLxhkZiG1jGLNiRDuXYJBnZjEfHjS48"
CHAT_ID = "1144838994"
bot = telebot.TeleBot(BOT_TOKEN)

def send_to_telegram(file_path, caption=""):
    with open(file_path, "rb") as f:
        bot.send_photo(CHAT_ID, f, caption=caption)

# --- Function to capture screenshots ---
def capture_screenshots():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.coinglass.com/pro/futures/LiquidationMap")

    # Scroll down slightly
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(2)

    # 1 day screenshot
    filename_day1 = "1_day.png"
    driver.save_screenshot(filename_day1)
    send_to_telegram(filename_day1, "Liquidation Map - 1 day")
    print("✅ Captured 1 day")

    # Click 1 day button to open dropdown
    try:
        button_1day = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'1 day')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", button_1day)
        driver.execute_script("arguments[0].click();", button_1day)
        time.sleep(1)
    except Exception as e:
        print(f"❌ Could not click 1 day button: {e}")

    # Click 7 day button
    try:
        button_7days = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//li[contains(text(),'7 day')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", button_7days)
        driver.execute_script("arguments[0].click();", button_7days)
        time.sleep(5)

        filename_7days = "7_days.png"
        driver.save_screenshot(filename_7days)
        send_to_telegram(filename_7days, "Liquidation Map - 7 days")
        print("✅ Captured 7 days")

    except Exception as e:
        print(f"❌ Could not capture 7 days: {e}")

    driver.quit()


# --- Run every 1 minute ---
while True:
    capture_screenshots()
    print("⏱ Waiting 1 minute before next capture...")
    time.sleep(60)
