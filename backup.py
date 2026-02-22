import os
import zipfile
import json
import requests
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime

# مسیر فولدرها برای بکاپ
VAR_PATH = "/var/lib/marzban"
OPT_PATH = "/opt/marzban"

CONFIG_FILE = "config.json"

# خواندن تنظیمات کاربر
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

telegram_token = config["token"]
chat_id = config["chat_id"]
user_caption = config["caption"]

# لینک GitHub پروژه
GITHUB_LINK = "https://github.com/MrTabahkar/Marzban-backup"

# دریافت IP سرور
def get_server_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except requests.RequestException:
        import socket
        return socket.gethostbyname(socket.gethostname())

server_ip = get_server_ip()

# متن اسپانسر لینک دار HTML
SPONSOR_TEXT = '<a href="https://t.me/MOTFKRM">ساخت پنل نمایندگی V2Ray با بهترین قیمت و بهترین متود ها!</a>'

# ترکیب کپشن نهایی
caption = (
    f"📂From {server_ip}\n"
    f"⛓️‍💥 {user_caption}\n"
    f"➖➖➖➖GitHub➖➖➖➖\n{GITHUB_LINK}\n\n"
    f"➖➖➖➖Sponsor➖➖➖➖\n{SPONSOR_TEXT}"
)

bot = Bot(token=telegram_token)

# فایل بکاپ با timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_ZIP = f"marzban_backup_{timestamp}.zip"

# ساخت بکاپ
def create_backup():
    with zipfile.ZipFile(BACKUP_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in [VAR_PATH, OPT_PATH]:
            if not os.path.exists(folder):
                print(f"❌ Path does not exist: {folder}")
                continue
            for root, dirs, files in os.walk(folder):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, start="/")
                    zipf.write(abs_path, rel_path)
    print(f"✅ Backup created: {BACKUP_ZIP}")

# ارسال بکاپ به تلگرام
def send_backup():
    try:
        with open(BACKUP_ZIP, "rb") as f:
            bot.send_document(
                chat_id=chat_id,
                document=f,
                caption=caption,
                parse_mode="HTML"
            )
        print("✅ Backup sent to Telegram successfully!")
    except TelegramError as e:
        print(f"❌ Telegram error: {e}")

# حذف فایل زیپ بعد از ارسال
def cleanup():
    if os.path.exists(BACKUP_ZIP):
        os.remove(BACKUP_ZIP)
        print(f"🗑 Backup file {BACKUP_ZIP} removed from server.")

if __name__ == "__main__":
    create_backup()
    send_backup()
    cleanup()