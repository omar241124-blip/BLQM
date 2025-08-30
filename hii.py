import time
import telebot

# --- Telegram setup ---
BOT_TOKEN = "8242720791:AAEtNLxhkZiG1jGLNiRDuXYJBnZjEfHjS48"
CHAT_ID = "1144838994"
bot = telebot.TeleBot(BOT_TOKEN)

print("Bot started. Sending 'Hi' every 1 minute...")

while True:
    try:
        bot.send_message(CHAT_ID, "Hi")
        print("✅ Sent 'Hi' to Telegram")
    except telebot.apihelper.ApiException as e:
        print(f"❌ Telegram API error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    time.sleep(60)  # wait 1 minute before sending again
