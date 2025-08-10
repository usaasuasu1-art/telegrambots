@echo off
echo 🤖 Starting Telegram Media Downloader Bot...

REM Check if config.py exists
if not exist "config.py" (
    echo ❌ config.py not found!
    echo Please copy config_example.py to config.py and add your credentials
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found!
    pause
    exit /b 1
)

REM Run the bot
echo 🚀 Bot is starting...
python main.py
pause