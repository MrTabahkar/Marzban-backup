#!/bin/bash

set -e

echo "🔄 Updating server packages..."
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip zip curl

# بررسی virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "✅ Activating virtual environment..."
source venv/bin/activate

# نصب پیش‌نیازها
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# گرفتن اطلاعات از کاربر
while [[ -z "$tk" ]]; do
    read -rp "Bot token: " tk
done

while [[ -z "$chatid" ]]; do
    read -rp "Chat ID: " chatid
done

read -rp "Caption (for backup identification): " caption

echo "Cronjob format:"
echo " - For every N minutes: just type the number (e.g. 5)"
echo " - For every N hours: type '0 N' (e.g. 0 5 for every 5 hours)"
while true; do
    read -rp "Enter cron time (minutes hours): " minute hour
    if [[ -z "$minute" ]]; then
        echo "Please enter a valid cron time."
        continue
    fi
    if [[ -z "$hour" ]]; then
        cron_time="*/$minute * * * *"
        break
    else
        cron_time="$minute */$hour * * *"
        break
    fi
done

# ذخیره مقادیر در config.json
cat > config.json <<EOL
{
    "token": "$tk",
    "chat_id": "$chatid",
    "caption": "$caption"
}
EOL

# حذف کرون قبلی مرتبط با backup.py
sudo crontab -l | grep -v 'backup.py' | crontab -

# اضافه کردن کرون جاب جدید
(crontab -l 2>/dev/null; echo "$cron_time cd $(pwd) && /bin/bash -c 'source venv/bin/activate && python3 backup.py' >/dev/null 2>&1") | crontab -

echo "⏱️ Cronjob added: $cron_time"

# اجرای بکاپ اولیه
echo "🚀 Running first backup..."
python3 backup.py

echo "🎉 Setup complete! Backup script will now run automatically based on your cron settings."