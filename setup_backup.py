import json
import os
import getpass

CONFIG_FILE = "config.json"

print("="*50)
print("MOTFKRM Telegram Backup Setup")
print("="*50)

# تابع برای گرفتن عدد مثبت از کاربر
def get_positive_int(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("❌ Please enter a valid positive integer.")

# گرفتن اطلاعات از کاربر
def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ Input cannot be empty.")

telegram_token = get_non_empty_input("Enter your Telegram Bot Token: ")
chat_id = get_non_empty_input("Enter your Telegram Chat ID (numbers only): ")
caption = get_non_empty_input("Enter your custom caption for backup: ")
interval_hours = get_positive_int("Enter backup interval in hours (e.g., 2): ")

# ذخیره تنظیمات در config.json
config_data = {
    "token": telegram_token,
    "chat_id": chat_id,
    "caption": caption,
    "interval_hours": interval_hours
}

with open(CONFIG_FILE, "w") as f:
    json.dump(config_data, f, indent=4)

print(f"\n✅ Settings saved to {CONFIG_FILE}.")

# اضافه کردن Cron job
script_path = os.path.abspath("backup.py")

# ایجاد ساعات Cron بر اساس فاصله ساعتی
cron_hours = ','.join(str(h) for h in range(0, 24, interval_hours))
cron_command = f"0 {cron_hours} * * * /usr/bin/python3 {script_path} > /dev/null 2>&1"

# اضافه کردن به کرون کاربر
os.system(f'(crontab -l 2>/dev/null; echo "{cron_command}") | crontab -')

print(f"✅ Cron job scheduled every {interval_hours} hours at minute 0.")
print("\nSetup complete! Your backups will run automatically every interval.")