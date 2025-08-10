@echo off
echo 🚀 Installing Telegram Media Downloader Bot...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Check if ffmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  ffmpeg is not installed.
    echo Please download ffmpeg from https://ffmpeg.org/download.html
    echo and add it to your system PATH
) else (
    echo ✅ ffmpeg is already installed
)

REM Create config file if it doesn't exist
if not exist "config.py" (
    echo 📝 Creating config.py from template...
    copy config_example.py config.py
    echo ⚠️  Please edit config.py and add your bot token, API ID, and API Hash
) else (
    echo ✅ config.py already exists
)

echo.
echo 🎉 Installation completed!
echo.
echo 📋 Next steps:
echo 1. Edit config.py and add your credentials
echo 2. Run the bot: python main.py
echo.
echo 📖 For more information, see README.md
pause