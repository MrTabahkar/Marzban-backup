#!/bin/bash
set -e

# ==========================
# @MOTFKRM Alireza Anari 
# ==========================
RED="\033[91m"
GREEN="\033[92m"
YELLOW="\033[93m"
BLUE="\033[94m"
PURPLE="\033[95m"
CYAN="\033[96m"
BOLD="\033[1m"
RESET="\033[0m"

type_text() {
    local text="$1"
    local delay="${2:-0.05}"
    for ((i=0; i<${#text}; i++)); do
        echo -ne "${text:$i:1}"
        sleep "$delay"
    done
    echo
}

blink_intro() {
    for i in {1..10}; do
        clear
        echo -e "${RED}${BOLD}╔════════════════════════════════╗${RESET}"
        type_text "${GREEN}${BOLD}         BackUp ALiREZA         ${RESET}" 0.08
        type_text "${CYAN}${BOLD}     Developer: @MOTFKRM       ${RESET}" 0.06
        echo -e "${RED}${BOLD}╚════════════════════════════════╝${RESET}"
        sleep 0.5
        clear
        sleep 0.3
    done
}

blink_intro

echo -e "${YELLOW}🔄 Updating server packages...${RESET}"
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip zip curl

# بررسی virtual environment
if [ ! -d "venv" ]; then
    echo -e "${CYAN}📦 Creating Python virtual environment...${RESET}"
    python3 -m venv venv
fi

echo -e "${GREEN}✅ Activating virtual environment...${RESET}"
source venv/bin/activate

# نصب پیش‌نیازها
echo -e "${YELLOW}📥 Installing Python dependencies...${RESET}"
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

echo -e "${CYAN}⏱️ Cronjob format:${RESET}"
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

echo -e "${GREEN}⏱️ Cronjob added: $cron_time${RESET}"

# اجرای بکاپ اولیه
echo -e "${CYAN}🚀 Running first backup...${RESET}"
python3 backup.py

echo -e "${GREEN}🎉 Setup complete! Backup script will now run automatically based on your cron settings.${RESET}"