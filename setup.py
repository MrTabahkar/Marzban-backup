import os
import subprocess

print("="*50)
print("MOTFKRM Marzban Backup Installer")
print("="*50)

# نصب python-telegram-bot
print("Installing required packages...")
subprocess.run(["pip3", "install", "--upgrade", "pip"])
subprocess.run(["pip3", "install", "python-telegram-bot==13.21"])

# اجرای setup اولیه
print("\nRunning setup_backup.py to configure your bot...")
os.system("python3 setup_backup.py")

print("\nInstallation and setup complete!")