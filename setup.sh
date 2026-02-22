#!/bin/bash

# ======================================================
# MOTFKRM Marzban Backup Installer
# ======================================================

echo "=================================================="
echo "MOTFKRM Marzban Backup Installer"
echo "=================================================="

# ساخت venv
if [ ! -d "venv" ]; then
    echo "🛠 Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists."
fi

# فعال کردن venv
echo "⚡️ Activating virtual environment..."
source venv/bin/activate

# بروزرسانی pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# نصب پیش‌نیازها
if [ -f "requirements.txt" ]; then
    echo "📦 Installing required packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# اجرای setup_backup.py برای گرفتن اطلاعات کاربر
echo "📝 Running setup_backup.py to configure your bot..."
python3 setup_backup.py

# اجرای یکبار backup.py برای تست
echo "🚀 Running backup.py to test sending backup..."
python3 backup.py

echo "=================================================="
echo "✅ Installation and setup complete!"
echo "Your backups will now run automatically via cron job at the interval you specified."
echo "=================================================="

# اتمام script
deactivate