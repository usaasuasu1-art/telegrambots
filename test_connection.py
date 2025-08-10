#!/usr/bin/env python3
"""
Test script untuk memverifikasi koneksi bot dan API Telegram
"""

import asyncio
import aiohttp
from telethon import TelegramClient

# Import config
try:
    from config import BOT_TOKEN, API_ID, API_HASH
except ImportError:
    print("❌ config.py tidak ditemukan!")
    print("Silakan copy config_example.py ke config.py dan isi kredensial Anda")
    exit(1)

async def test_bot_api():
    """Test koneksi ke Telegram Bot API"""
    print("🔍 Testing Bot API...")
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('ok'):
                        bot_info = data['result']
                        print(f"✅ Bot API OK")
                        print(f"   Bot Name: {bot_info.get('first_name')}")
                        print(f"   Username: @{bot_info.get('username')}")
                        print(f"   Bot ID: {bot_info.get('id')}")
                        return True
                    else:
                        print(f"❌ Bot API Error: {data.get('description')}")
                        return False
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Bot API Error: {str(e)}")
        return False

async def test_telegram_api():
    """Test koneksi ke Telegram Client API"""
    print("\n🔍 Testing Telegram Client API...")
    
    try:
        # Convert API_ID to int if needed
        api_id = int(API_ID) if isinstance(API_ID, str) else API_ID
        
        client = TelegramClient('test_session', api_id, API_HASH)
        await client.start()
        
        me = await client.get_me()
        if me:
            print(f"✅ Telegram Client API OK")
            print(f"   User ID: {me.id}")
            print(f"   Username: @{me.username}")
            print(f"   First Name: {me.first_name}")
        else:
            print("❌ Tidak bisa mendapatkan info user")
            return False
        
        await client.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Telegram Client API Error: {str(e)}")
        return False

async def test_telegram_link():
    """Test parsing Telegram link"""
    print("\n🔍 Testing Telegram link parsing...")
    
    test_link = "https://t.me/test_channel/123"
    
    try:
        import re
        pattern = r'https://t\.me/([^/]+)/(\d+)'
        match = re.match(pattern, test_link)
        
        if match:
            channel_username = match.group(1)
            message_id = int(match.group(2))
            print(f"✅ Link parsing OK")
            print(f"   Channel: {channel_username}")
            print(f"   Message ID: {message_id}")
            return True
        else:
            print("❌ Link parsing failed")
            return False
            
    except Exception as e:
        print(f"❌ Link parsing error: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Testing Telegram Media Downloader Bot Configuration")
    print("=" * 50)
    
    # Test Bot API
    bot_ok = await test_bot_api()
    
    # Test Telegram Client API
    client_ok = await test_telegram_api()
    
    # Test link parsing
    link_ok = await test_telegram_link()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Bot API: {'✅ OK' if bot_ok else '❌ FAILED'}")
    print(f"   Client API: {'✅ OK' if client_ok else '❌ FAILED'}")
    print(f"   Link Parsing: {'✅ OK' if link_ok else '❌ FAILED'}")
    
    if bot_ok and client_ok and link_ok:
        print("\n🎉 Semua test berhasil! Bot siap digunakan.")
        print("Jalankan: python main.py")
    else:
        print("\n⚠️  Beberapa test gagal. Silakan periksa konfigurasi Anda.")
        
        if not bot_ok:
            print("   - Periksa BOT_TOKEN di config.py")
        if not client_ok:
            print("   - Periksa API_ID dan API_HASH di config.py")
        if not link_ok:
            print("   - Ada masalah dengan parsing link")

if __name__ == "__main__":
    asyncio.run(main())