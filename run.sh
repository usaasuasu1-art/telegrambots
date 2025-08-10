#!/bin/bash

echo "🤖 Starting Telegram Media Downloader Bot..."

# Check if config.py exists
if [ ! -f "config.py" ]; then
    echo "❌ config.py not found!"
    echo "Please copy config_example.py to config.py and add your credentials"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    exit 1
fi

# Run the bot
echo "🚀 Bot is starting..."
python3 main.py