#!/bin/bash

echo "🚀 Installing Telegram Media Downloader Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg is not installed. Installing ffmpeg..."
    
    # Detect OS and install ffmpeg
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        else
            echo "❌ Could not install ffmpeg automatically. Please install it manually."
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ Homebrew not found. Please install ffmpeg manually: brew install ffmpeg"
        fi
    else
        echo "❌ Unsupported OS. Please install ffmpeg manually."
    fi
else
    echo "✅ ffmpeg is already installed"
fi

# Create config file if it doesn't exist
if [ ! -f "config.py" ]; then
    echo "📝 Creating config.py from template..."
    cp config_example.py config.py
    echo "⚠️  Please edit config.py and add your bot token, API ID, and API Hash"
else
    echo "✅ config.py already exists"
fi

echo ""
echo "🎉 Installation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit config.py and add your credentials"
echo "2. Run the bot: python3 main.py"
echo ""
echo "📖 For more information, see README.md"