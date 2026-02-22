import json
import os
import getpass

CONFIG_FILE = "config.json"

print("="*50)
print("MOTFKRM Telegram Backup Setup")
print("="*50)

# گرفتن اطلاعات از کاربر
telegram_token = input("Enter your Telegram Bot Token: ").strip()
chat_id = input("Enter your Telegram Chat ID (numbers only): ").strip()
user_caption = input("Enter your custom caption for backup: ").strip()
interval_hours = int(input("Enter backup interval in hours (e.g., 2): ").strip())

# ذخیره تنظیمات در config.json
config_data = {
    "telegram_token": telegram_token,
    "chat_id": chat_id,
    "user_caption": user_caption,
    "interval_hours": interval_hours
}

with open(CONFIG_FILE, "w") as f:
    json.dump(config_data, f, indent=4)

print(f"\nSettings saved to {CONFIG_FILE}.")

# اضافه کردن Cron job
user = getpass.getuser()
script_path = os.path.abspath("backup.py")

# ایجاد ساعات Cron بر اساس فاصله ساعتی
cron_hours = ','.join(str(h) for h in range(0, 24, interval_hours))
cron_command = f"0 {cron_hours} * * * /usr/bin/python3 {script_path}"

# اضافه کردن به کرون کاربر
os.system(f'(crontab -l 2>/dev/null; echo "{cron_command}") | crontab -')
print(f"Cron job scheduled every {interval_hours} hours at minute 0.")
print("\nSetup complete! Your backups will run automatically every interval.")