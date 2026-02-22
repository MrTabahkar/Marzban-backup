#!/bin/bash

echo "=================================================="
echo "MOTFKRM Marzban Backup Installer (One Command)"
echo "=================================================="

# بررسی نصب python3-venv و python3-pip
echo "Checking for required system packages..."
sudo apt update
sudo apt install -y python3-venv python3-pip

# ساخت venv
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# فعال کردن venv
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# بروزرسانی pip و نصب پیش نیازها
echo "Upgrading pip..."
pip install --upgrade pip
echo "Installing required Python packages..."
pip install -r requirements.txt

# اجرای setup_backup.py برای گرفتن اطلاعات کاربر
echo ""
echo "Running setup_backup.py to configure your bot..."
python3 setup_backup.py

# اجرای backup.py یکبار برای تست
echo ""
echo "Running backup.py once to test backup..."
python3 backup.py

echo ""
echo "=================================================="
echo "Setup complete! Your backups will run automatically according to your chosen cron schedule."
echo "To manually run backup anytime: source venv/bin/activate && python3 backup.py"
echo "=================================================="