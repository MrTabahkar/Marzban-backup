#!/usr/bin/env python3
import os
import zipfile
import json
import subprocess
import asyncio
import requests
from telegram import Bot
from telegram.error import TelegramError
#==========================
# Developer @MOTFKRM
#==========================
# مسیرها

VAR_PATH = "/var/lib/marzban"
OPT_PATH = "/opt/marzban"
MYSQL_BACKUP_DIR = "/var/lib/marzban/mysql/db-backup"
ENV_FILE = "/opt/marzban/.env"
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
caption = f"📂 From {server_ip}\n⛓️ {user_caption}\n@MOTFKRM GitHub: https://github.com/MrTabahkar/Marzban-backup"


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
    dump_file = os.path.join(MYSQL_BACKUP_DIR, "marzban.sql")
    print(f"🛢 Dumping MySQL to {dump_file} ...")
    cmd = f"docker exec marzban-mysql-1 mysqldump -uroot -p{MYSQL_ROOT_PASSWORD} --routines marzban > {dump_file}"
    subprocess.run(cmd, shell=True, check=True)
    print(f"✅ MySQL dump created at {dump_file}")


# اضافه کردن پوشه‌ها به zip

def add_folder_to_zip(zipf, folder_path, ignore_mysql_files=False):
    for root_dir, dirs, files in os.walk(folder_path):
        
        if ignore_mysql_files and os.path.basename(root_dir) == "mysql":
            dirs[:] = ["db-backup"] if "db-backup" in dirs else []
            files[:] = []
        for file in files:
            abs_path = os.path.join(root_dir, file)
            rel_path = os.path.relpath(abs_path, start="/")
            size_mb = os.path.getsize(abs_path) / 1024 / 1024
            print(f"📂 Adding {rel_path} ({size_mb:.2f} MB)")
            zipf.write(abs_path, rel_path)


# ساخت پارت‌های zip

def create_zip_parts():
    backup_mysql()  

    # مسیر موقت برای zip
    temp_zip = "marzban_temp.zip"
    with zipfile.ZipFile(temp_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        add_folder_to_zip(zipf, VAR_PATH, ignore_mysql_files=True)
        
        for root_dir, dirs, files in os.walk(OPT_PATH):
            for file in files:
                abs_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(abs_path, start="/")
                size_mb = os.path.getsize(abs_path) / 1024 / 1024
                print(f"📂 Adding {rel_path} ({size_mb:.2f} MB)")
                zipf.write(abs_path, rel_path)

    total_size = os.path.getsize(temp_zip) / 1024 / 1024
    print(f"📊 Total backup size: {total_size:.2f} MB")

    if total_size <= 50:
        final_name = "Marzban1.zip"
        os.rename(temp_zip, final_name)
        return [final_name]
    else:
        
        part1 = "Marzban1.zip"
        part2 = "Marzban2.zip"
        with zipfile.ZipFile(temp_zip, "r") as zip_read:
            all_files = zip_read.namelist()
            half = len(all_files) // 2
            with zipfile.ZipFile(part1, "w", zipfile.ZIP_DEFLATED) as z1:
                for f in all_files[:half]:
                    z1.writestr(f, zip_read.read(f))
            with zipfile.ZipFile(part2, "w", zipfile.ZIP_DEFLATED) as z2:
                for f in all_files[half:]:
                    z2.writestr(f, zip_read.read(f))
        os.remove(temp_zip)
        return [part1, part2]


# ارسال پارت‌ها به تلگرام

async def send_parts_to_telegram(parts):
    for p in parts:
        size_mb = os.path.getsize(p) / 1024 / 1024
        print(f"📤 Sending {p} ({size_mb:.2f} MB) to Telegram...")
        try:
            with open(p, "rb") as f:
                await bot.send_document(chat_id=chat_id, document=f, caption=caption)
            print(f"✅ {p} sent to Telegram successfully!")
        except TelegramError as e:
            print(f"❌ Telegram error: {e}")
        os.remove(p)
        print(f"🗑 {p} removed from server.")

# اجرا
if __name__ == "__main__":
    parts = create_zip_parts()
    asyncio.run(send_parts_to_telegram(parts))
    print("🎉 Backup completed!")
