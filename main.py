
import os
import asyncio
import tempfile
import shutil
import aiohttp
import json
import yt_dlp
from urllib.parse import quote

# Bot token dari BotFather
BOT_TOKEN = "7996057828:AAGpzZPMVVUs7qSqyZcwOY4Etn7xtbffNuE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def send_message(self, chat_id, text, parse_mode=None):
        data = {
            'chat_id': chat_id,
            'text': text
        }
        if parse_mode:
            data['parse_mode'] = parse_mode
        
        async with self.session.post(f"{self.api_url}/sendMessage", data=data) as response:
            return await response.json()
    
    async def send_audio(self, chat_id, audio_file_path, title=None, performer=None, thumbnail_path=None):
        data = aiohttp.FormData()
        data.add_field('chat_id', str(chat_id))
        
        if title:
            data.add_field('title', title)
        if performer:
            data.add_field('performer', performer)
        
        # Read audio file
        with open(audio_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        data.add_field('audio', audio_data, filename=os.path.basename(audio_file_path))
        
        # Read thumbnail file if exists
        if thumbnail_path and os.path.exists(thumbnail_path):
            with open(thumbnail_path, 'rb') as thumb_file:
                thumb_data = thumb_file.read()
            data.add_field('thumb', thumb_data, filename=os.path.basename(thumbnail_path))
        
        async with self.session.post(f"{self.api_url}/sendAudio", data=data) as response:
            return await response.json()
    
    async def get_chat_member(self, chat_id, user_id):
        """Get information about a chat member"""
        data = {
            'chat_id': chat_id,
            'user_id': user_id
        }
        async with self.session.post(f"{self.api_url}/getChatMember", data=data) as response:
            return await response.json()
    
    async def get_me(self):
        """Get bot information"""
        async with self.session.get(f"{self.api_url}/getMe") as response:
            return await response.json()
    
    async def edit_message_text(self, chat_id, message_id, text, parse_mode=None):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text
        }
        if parse_mode:
            data['parse_mode'] = parse_mode
        
        async with self.session.post(f"{self.api_url}/editMessageText", data=data) as response:
            return await response.json()
    
    async def delete_message(self, chat_id, message_id):
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        async with self.session.post(f"{self.api_url}/deleteMessage", data=data) as response:
            return await response.json()
    
    async def get_updates(self, offset=None, timeout=30):
        params = {'timeout': timeout}
        if offset:
            params['offset'] = offset
        
        async with self.session.get(f"{self.api_url}/getUpdates", params=params) as response:
            return await response.json()
    
    async def set_my_commands(self, commands):
        """Set bot commands for menu suggestions"""
        data = {
            'commands': json.dumps(commands)
        }
        
        async with self.session.post(f"{self.api_url}/setMyCommands", data=data) as response:
            return await response.json()

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '0',  # Best quality
            'outtmpl': '%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'writethumbnail': True,
        }

    async def search_and_download(self, query, output_dir):
        """Search for a song and download the first result"""
        try:
            search_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                # Search for the query
                search_results = ydl.extract_info(f"ytsearch1:{query}", download=False)
                
                if not search_results or 'entries' not in search_results or not search_results['entries']:
                    return None, None, None, "❌ Tidak ditemukan hasil untuk pencarian tersebut."
                
                # Get the first result
                first_result = search_results['entries'][0]
                video_id = first_result['id']
                
                # Construct proper YouTube URL
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Now download using the URL
                return await self.download_audio(video_url, output_dir)
                
        except Exception as e:
            return None, None, None, f"❌ Error dalam pencarian: {str(e)}"

    async def download_audio(self, url, output_dir):
        """Download audio from YouTube URL"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                channel = info.get('channel', info.get('uploader', 'Unknown Artist'))
                artist = info.get('artist', info.get('creator', channel))
                
                # Check duration (max 10 minutes = 600 seconds)
                if duration > 600:
                    return None, None, None, "❌ Video terlalu panjang! Maksimal 10 menit."
                
                # Set output path
                filename = f"{title}.%(ext)s"
                self.ydl_opts['outtmpl'] = os.path.join(output_dir, filename)
                
                # Download
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl_download:
                    ydl_download.download([url])
                
                # Find downloaded files
                audio_path = None
                thumbnail_path = None
                
                for file in os.listdir(output_dir):
                    if file.startswith(title):
                        if file.endswith(('.jpg', '.png', '.webp')):
                            thumbnail_path = os.path.join(output_dir, file)
                        else:
                            original_path = os.path.join(output_dir, file)
                            mp3_path = os.path.join(output_dir, f"{title}.mp3")
                            
                            # Convert to MP3 using ffmpeg
                            await self.convert_to_mp3(original_path, mp3_path)
                            
                            # Remove original if different
                            if original_path != mp3_path and os.path.exists(original_path):
                                os.remove(original_path)
                            
                            audio_path = mp3_path
                
                if not audio_path:
                    return None, None, None, "❌ File tidak ditemukan setelah download."
                
                return audio_path, thumbnail_path, artist, title
                
        except Exception as e:
            return None, None, None, f"❌ Error: {str(e)}"

    async def convert_to_mp3(self, input_path, output_path):
        """Convert audio to MP3 using ffmpeg"""
        if input_path.endswith('.mp3'):
            if input_path != output_path:
                shutil.move(input_path, output_path)
            return
        
        cmd = [
            'ffmpeg', '-i', input_path,
            '-acodec', 'libmp3lame',
            '-q:a', '0',  # Variable bitrate, best quality (equivalent to ~245kbps)
            '-y',  # Overwrite output file
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

async def send_command_suggestions(bot, chat_id):
    """Send command suggestions"""
    suggestions_text = "🎵 Kirim URL YouTube atau nama lagu untuk download audio\n\nContoh:\n/yt https://youtube.com/watch?v=...\n/yt cukup\n/yt dewa 19 risalah hati"
    
    # Create custom keyboard with command suggestion
    keyboard = {
        "keyboard": [
            [{"text": "/yt "}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
        "input_field_placeholder": "YouTube URL atau nama lagu..."
    }
    
    data = {
        'chat_id': chat_id,
        'text': suggestions_text,
        'reply_markup': json.dumps(keyboard)
    }
    
    async with bot.session.post(f"{bot.api_url}/sendMessage", data=data) as response:
        return await response.json()

async def handle_youtube_download(bot, chat_id, query):
    """Handle YouTube download or search"""
    # Check if it's a URL or search query
    is_url = 'youtube.com' in query or 'youtu.be' in query
    
    if is_url:
        processing_msg = "🔄 Memproses URL... Mohon tunggu sebentar."
    else:
        processing_msg = f"🔍 Mencari '{query}'... Mohon tunggu sebentar."
    
    # Send processing message
    processing_data = {
        'chat_id': chat_id,
        'text': processing_msg
    }
    
    async with bot.session.post(f"{bot.api_url}/sendMessage", data=processing_data) as response:
        processing_response = await response.json()
    
    processing_msg_id = processing_response['result']['message_id']
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    downloader = YouTubeDownloader()
    
    try:
        # Download audio (either from URL or search)
        if is_url:
            file_path, thumbnail_path, artist, title = await downloader.download_audio(query, temp_dir)
        else:
            file_path, thumbnail_path, artist, title = await downloader.search_and_download(query, temp_dir)
        
        if file_path and os.path.exists(file_path):
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Check file size (Telegram limit: 50MB)
            if file_size > 50 * 1024 * 1024:
                await bot.edit_message_text(chat_id, processing_msg_id, "❌ File terlalu besar! Maksimal 50MB.")
                return
            
            # Send the MP3 file
            await bot.edit_message_text(chat_id, processing_msg_id, "📤 Mengirim file...")
            
            await bot.send_audio(
                chat_id,
                file_path,
                title=title,
                performer=artist,
                thumbnail_path=thumbnail_path
            )
            
            await bot.delete_message(chat_id, processing_msg_id)
            
        else:
            await bot.edit_message_text(chat_id, processing_msg_id, title if isinstance(title, str) else "❌ Gagal mendownload file.")
    
    except Exception as e:
        await bot.edit_message_text(chat_id, processing_msg_id, f"❌ Terjadi error: {str(e)}")
    
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

async def process_update(bot, update):
    """Process incoming update"""
    # Handle both messages and channel posts
    message = None
    if 'message' in update:
        message = update['message']
    elif 'channel_post' in update:
        message = update['channel_post']
    
    if not message:
        return
    
    chat_id = message['chat']['id']
    message_id = message['message_id']
    chat_type = message['chat']['type']
    
    if 'text' not in message:
        return
    
    text = message['text']
    
    # For groups/supergroups, only respond to commands or mentions
    if chat_type in ['group', 'supergroup']:
        # Get bot info to check for mentions
        if not hasattr(bot, '_bot_username'):
            bot_info = await bot.get_me()
            if bot_info.get('ok'):
                bot._bot_username = f"@{bot_info['result']['username']}"
            else:
                bot._bot_username = "@" + BOT_TOKEN.split(':')[0] + "_bot"
        
        # Only respond if it's a command or bot is mentioned
        if not (text.startswith('/') or bot._bot_username in text):
            return
    
    # Handle commands
    if text.startswith('/start') or text.startswith('/help'):
        await send_command_suggestions(bot, chat_id)
    elif text.startswith('/yt ') or text.startswith('/yt@'):
        # Extract query, handling both /yt and /yt@botusername formats
        if text.startswith('/yt@'):
            parts = text.split(' ', 1)
            query = parts[1].strip() if len(parts) > 1 else ""
        else:
            query = text[4:].strip()
        
        if query:
            # Auto-delete user command for all chat types
            try:
                await asyncio.sleep(1)
                await bot.delete_message(chat_id, message_id)
            except:
                pass  # Ignore if can't delete (e.g., no admin rights)
            
            await handle_youtube_download(bot, chat_id, query)
        else:
            # Auto-delete invalid command for all chat types
            try:
                await asyncio.sleep(1)
                await bot.delete_message(chat_id, message_id)
            except:
                pass  # Ignore if can't delete
            await send_command_suggestions(bot, chat_id)

async def main():
    """Start the bot"""
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN tidak ditemukan!")
        print("Silakan set environment variable TELEGRAM_BOT_TOKEN dengan token bot Anda.")
        return
    
    print("🤖 Bot Telegram YouTube MP3 Downloader dimulai...")
    print("Tekan Ctrl+C untuk menghentikan bot.")
    
    async with TelegramBot(BOT_TOKEN) as bot:
        # Setup bot commands for suggestions menu
        commands = [
            {
                "command": "yt",
                "description": "Download audio dari YouTube - /yt [URL atau nama lagu]"
            }
        ]
        await bot.set_my_commands(commands)
        
        offset = None
        
        while True:
            try:
                # Get updates
                response = await bot.get_updates(offset=offset)
                
                if response.get('ok'):
                    updates = response.get('result', [])
                    
                    for update in updates:
                        # Process each update (handles both messages and channel posts)
                        await process_update(bot, update)
                        
                        # Update offset
                        offset = update['update_id'] + 1
                
                # Small delay to prevent API rate limiting
                await asyncio.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot dihentikan.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
