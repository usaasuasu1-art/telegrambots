# Changelog

## [1.0.0] - 2024-01-XX

### Added
- 🎵 **YouTube Audio Download**: Download audio dari YouTube dengan URL atau pencarian nama lagu
- 📱 **Telegram Media Fetch**: Ambil video/documents/foto dari channel Telegram menggunakan link
- 🤖 **Auto-cleanup**: Otomatis menghapus command user dan file temporary
- 📊 **File size check**: Validasi ukuran file (maksimal 50MB)
- 🎯 **Multi-format support**: Support berbagai format media (video, audio, document, photo)
- 🔧 **Command handling**: Support `/yt` dan `/tg` commands dengan username bot
- 📋 **Custom keyboard**: Keyboard dengan tombol command suggestion
- 🛡️ **Error handling**: Penanganan error yang lebih baik
- 📝 **Configuration management**: Support file config terpisah
- 🧪 **Test script**: Script untuk test koneksi dan konfigurasi
- 📦 **Installation scripts**: Script otomatis untuk instalasi di Linux/macOS/Windows
- 🚀 **Service support**: Systemd service untuk Linux
- 📖 **Comprehensive documentation**: README lengkap dengan troubleshooting

### Technical Features
- **Telethon integration**: Menggunakan Telethon library untuk akses Telegram API
- **Async/await**: Fully asynchronous implementation
- **Session management**: Proper session handling untuk Telethon client
- **File type detection**: Otomatis detect tipe file dan kirim dengan method yang sesuai
- **Link parsing**: Regex parsing untuk Telegram link format
- **Media info extraction**: Extract informasi file (nama, ukuran, tipe)
- **Temporary file management**: Proper cleanup temporary files
- **Rate limiting protection**: Delay untuk menghindari rate limiting

### Commands
- `/start` atau `/help` - Tampilkan menu bantuan
- `/yt [URL atau nama lagu]` - Download audio dari YouTube
- `/tg [link Telegram]` - Fetch media dari channel Telegram

### Supported Formats
- **YouTube**: URL YouTube atau pencarian nama lagu
- **Telegram**: Link format `https://t.me/channel_name/message_id`
- **Media Types**: Video, Audio, Document, Photo
- **File Formats**: MP4, AVI, MOV, MKV, WebM, MP3, JPG, PNG, PDF, dll

### Limitations
- Maksimal ukuran file: 50MB
- Maksimal durasi YouTube: 10 menit
- Hanya channel public atau yang sudah di-join
- Satu file per request

### Dependencies
- `aiohttp==3.9.1` - HTTP client untuk Telegram Bot API
- `yt-dlp==2023.12.30` - YouTube downloader
- `telethon==1.34.0` - Telegram client library
- `ffmpeg` - Audio converter (system dependency)

### Installation
- Script otomatis untuk Linux/macOS (`install.sh`)
- Script otomatis untuk Windows (`install.bat`)
- Manual installation dengan `pip install -r requirements.txt`

### Configuration
- File config terpisah (`config.py`)
- Template config (`config_example.py`)
- Environment variable support
- Test script untuk validasi kredensial

### Deployment
- Systemd service untuk Linux
- Script run untuk semua platform
- Auto-restart capability
- Log management