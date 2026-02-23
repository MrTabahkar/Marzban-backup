# MOTFKRM Marzban Backup

**For Persian speakers:** see [README-FA.md](README-FA.md) for instructions in Farsi.

# Marzban Telegram Backup Bot

This project is an automated Telegram backup bot for important Marzban directories:

- /var/lib/marzban
- /opt/marzban

Backups are automatically created and sent to your Telegram at the interval you specify.  
After sending, the zip file is automatically deleted from the server.

## Features

- Automatic backup of Marzban folders  
- Send backups to Telegram with your own bot token and chat_id  
- Captions include:
  - Server IP
  - User caption
  - GitHub link  
- Automatic Cron job for scheduled backups  
- Easy setup with a single command

## Requirements

- Python 3.x  
- python-telegram-bot library (installed automatically during setup)

## Easy Installation

Simply run the following commands on your server:

`git clone https://github.com/MrTabahkar/Marzban-backup.git&&cd Marzban-backup&&bash setup.sh`

During `setup.sh` execution, the following information will be requested:

1. Telegram bot token  
2. Numeric Chat ID  
3. Custom caption  
4. Backup interval (e.g., every 2 hours)

After that, a Cron job is automatically created and backups will run at the specified interval.

## Manual Backup (Optional)

`source venv/bin/activate&&python3 backup.py`
## Notes

- config.json stores token, chat_id, and user caption  
- Cron job runs according to the interval, no need to keep the script running  
- Zip file is deleted after sending each backup


## Disclaimer & Future Plans

This project is currently intended for **personal use only** and was not initially designed for public distribution.  

The main goal was to create a simple and functional backup bot for private use.  

However, we hope that in the future the project can be **expanded and improved** with additional features, broader compatibility, and enhanced automation.

## Support

⛓️‍💥GitHub: [Marzban-Backup](https://github.com/MrTabahkar/Marzban-backup)
📱 Telegram: [@MOTFKRM](https://t.me/MOTFKRM)  
📢 Channel: [@TFKORAT](https://t.me/TFKORAT)