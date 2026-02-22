# Marzban Telegram Backup Bot
# programmer @MOTFKRM (version -- 1.0.0)

این پروژه یک ربات خودکار بکاپ تلگرام برای پوشه‌های `/var/lib/marzban` و `/opt/marzban` است.  
با این ابزار، هر فاصله ساعتی که مشخص کنید، بکاپ ساخته شده و به تلگرام شما ارسال می‌شود.

## ویژگی‌ها
- بکاپ خودکار پوشه‌ها `/var/lib/marzban` و `/opt/marzban`
- ارسال به تلگرام با توکن و chat_id دلخواه
- کپشن شامل **کپشن کاربر + اسپانسر ثابت شما**
- Cron job خودکار برای اجرای منظم
- بعد از ارسال بکاپ، فایل زیپ روی سرور حذف می‌شود
- آماده اجرا با یک دستور (GitHub-ready)

## پیش‌نیازها
- Python 3.x
- نصب کتابخانه `python-telegram-bot`:

```bash
pip install python-telegram-bot