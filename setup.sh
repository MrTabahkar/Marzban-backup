#!/bin/bash

# =========================================================
# MOTFKRM Marzban Backup Installer
# =========================================================

echo "=================================================="
echo "MOTFKRM Marzban Backup Installer"
echo "=================================================="

# === متغیرها ===
VENV_DIR="venv"
REQUIREMENTS="requirements.txt"
BACKUP_SCRIPT="backup.py"

# === ۱. ساخت venv و فعال‌سازی ===
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# === ۲. بروزرسانی pip و نصب پیش‌نیازها ===
echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing required packages..."
pip install -r "$REQUIREMENTS"

# === ۳. گرفتن اطلاعات از کاربر ===
read -p "Enter your Telegram Bot Token: " TOKEN
read -p "Enter your Telegram Chat ID (numbers only): " CHAT_ID
read -p "Enter your custom caption for backup: " CAPTION
read -p "Enter backup interval in hours (e.g., 2): " INTERVAL_HOURS

# === ۴. ذخیره config.json ===
cat > config.json <<EOL
{
    "token": "$TOKEN",
    "chat_id": $CHAT_ID,
    "caption": "$CAPTION",
    "interval_hours": $INTERVAL_HOURS
}
EOL

echo "Settings saved to config.json."

# === ۵. اجرای یکبار backup.py ===
echo "Running initial backup..."
python3 "$BACKUP_SCRIPT"

# === ۶. تنظیم Cron Job ===
CRON_CMD="0 */$INTERVAL_HOURS * * * cd $(pwd) && $VENV_DIR/bin/python3 $BACKUP_SCRIPT"
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo "Cron job scheduled every $INTERVAL_HOURS hours."
echo "=================================================="
echo "Setup complete! Your backups will run automatically."