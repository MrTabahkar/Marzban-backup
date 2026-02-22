import os
import subprocess
import sys

print("="*50)
print("MOTFKRM Marzban Backup Installer")
print("="*50)

# 1️⃣ ساخت venv اگر وجود ندارد
VENV_DIR = "venv"
if not os.path.exists(VENV_DIR):
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR])

# 2️⃣ فعال کردن venv
activate_script = os.path.join(VENV_DIR, "bin", "activate_this.py")
if os.path.exists(activate_script):
    # فعال کردن venv در همان فرآیند پایتون
    with open(activate_script) as f:
        exec(f.read(), dict(__file__=activate_script))
else:
    print("⚠️ Could not find activate script, continuing...")

# مسیر pip داخل venv
pip_exe = os.path.join(VENV_DIR, "bin", "pip")

# 3️⃣ بروزرسانی pip
print("Upgrading pip...")
subprocess.run([pip_exe, "install", "--upgrade", "pip"])

# 4️⃣ نصب پیش نیازها
print("Installing required packages from requirements.txt...")
subprocess.run([pip_exe, "install", "-r", "requirements.txt"])

# 5️⃣ اجرای setup_backup.py برای گرفتن تنظیمات کاربر
print("\nRunning setup_backup.py to configure your bot...")
subprocess.run([sys.executable, "setup_backup.py"])

# 6️⃣ اجرای یکبار backup.py برای تست
print("\nRunning backup.py once to test backup...")
subprocess.run([sys.executable, "backup.py"])

print("\n✅ Installation and setup complete!")
print("Your backups will run automatically according to your chosen cron schedule.")