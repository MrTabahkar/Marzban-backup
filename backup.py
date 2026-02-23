import os
import zipfile
import json
import subprocess
from telegram import Bot
from telegram.error import TelegramError
import requests
import asyncio

# مسیرها
VAR_PATH = "/var/lib/marzban"
OPT_PATH = "/opt/marzban"
BACKUP_FILE = "marzban_backup.zip"
ENV_FILE = "/opt/marzban/.env"
MYSQL_BACKUP_DIR = "/var/lib/marzban/mysql/db-backup"

CONFIG_FILE = "config.json"

# خواندن تنظیمات تلگرام
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

telegram_token = config["token"]
chat_id = config["chat_id"]
user_caption = config.get("caption", "")

bot = Bot(token=telegram_token)

# گرفتن آی‌پی سرور
def get_server_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        import socket
        return socket.gethostbyname(socket.gethostname())

server_ip = get_server_ip()
caption = f"📂 From {server_ip}\n⛓️ {user_caption}\n@MOTFKRM GitHub : https://github.com/MrTabahkar/Marzban-backup"

# خواندن پسورد mysql از .env
def get_mysql_password(env_path=ENV_FILE):
    if not os.path.exists(env_path):
        return None
    with open(env_path) as f:
        for line in f:
            if line.startswith("MYSQL_ROOT_PASSWORD"):
                return line.strip().split("=", 1)[1]
    return None

MYSQL_ROOT_PASSWORD = get_mysql_password()
if MYSQL_ROOT_PASSWORD is None:
    print("❌ MYSQL_ROOT_PASSWORD not found in .env")
    exit(1)

# بکاپ دیتابیس
def backup_mysql():
    os.makedirs(MYSQL_BACKUP_DIR, exist_ok=True)
    try:
        # گرفتن لیست دیتابیس‌ها
        cmd_list_db = f"docker exec marzban-mysql-1 mysql -uroot -p{MYSQL_ROOT_PASSWORD} -e 'SHOW DATABASES;'"
        result = subprocess.run(cmd_list_db, shell=True, capture_output=True, text=True, check=True)
        databases = [db.strip() for db in result.stdout.splitlines() if db.strip() not in ("Database", "information_schema", "mysql", "performance_schema", "sys")]
        # بکاپ هر دیتابیس
        for db in databases:
            print(f"Dumping database: {db}")
            dump_cmd = f"docker exec marzban-mysql-1 mysqldump -uroot -p{MYSQL_ROOT_PASSWORD} --routines {db} > {MYSQL_BACKUP_DIR}/{db}.sql"
            subprocess.run(dump_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching databases: {e}")

# اضافه کردن var/lib/marzban به zip
def add_var_lib_marzban(zipf):
    for root, dirs, files in os.walk(VAR_PATH):
        if os.path.basename(root) == "mysql":
            dirs[:] = ["db-backup"] if "db-backup" in dirs else []
            files[:] = []
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, start="/")
            zipf.write(abs_path, rel_path)

# اضافه کردن opt/marzban به zip
def add_opt_marzban(zipf):
    for root, dirs, files in os.walk(OPT_PATH):
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, start="/")
            zipf.write(abs_path, rel_path)

# ساخت بکاپ
def create_backup():
    backup_mysql()  # اول بکاپ mysql
    with zipfile.ZipFile(BACKUP_FILE, "w", zipfile.ZIP_DEFLATED) as zipf:
        add_var_lib_marzban(zipf)
        add_opt_marzban(zipf)
    size_mb = os.path.getsize(BACKUP_FILE) / 1024 / 1024
    print(f"✅ Backup created: {BACKUP_FILE} ({size_mb:.2f} MB)")
    return BACKUP_FILE

# ارسال به تلگرام
async def send_backup(file_path):
    try:
        with open(file_path, "rb") as doc:
            await bot.send_document(chat_id=chat_id, document=doc, caption=caption)
        print("✅ Backup sent to Telegram successfully!")
    except TelegramError as e:
        print(f"❌ Telegram error: {e}")

# حذف فایل زیپ بعد از ارسال
def cleanup(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑 Backup file {file_path} removed from server.")

# اجرا
if __name__ == "__main__":
    backup_file = create_backup()
    asyncio.run(send_backup(backup_file))
    cleanup(backup_file)