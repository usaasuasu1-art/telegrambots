# Telegram Media Downloader Bot

Bot Telegram untuk mendownload audio dari YouTube dan mengambil media dari channel Telegram menggunakan link.

## Fitur

- 🎵 **YouTube Audio Download**: Download audio dari YouTube dengan URL atau pencarian nama lagu
- 📱 **Telegram Media Fetch**: Ambil video/documents/foto dari channel Telegram menggunakan link
- 🤖 **Auto-cleanup**: Otomatis menghapus command user dan file temporary
- 📊 **File size check**: Validasi ukuran file (maksimal 50MB)
- 🎯 **Multi-format support**: Support berbagai format media

📋 **Lihat [FEATURES.md](FEATURES.md) untuk detail lengkap fitur**

## Setup

### 1. Install Dependencies

**Opsi 1: Menggunakan script instalasi (Direkomendasikan)**

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
install.bat
```

**Opsi 2: Manual installation**

```bash
pip install -r requirements.txt
```

**Install ffmpeg (diperlukan untuk konversi audio):**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS/RHEL:**
```bash
sudo yum install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download dari [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) dan tambahkan ke PATH

### 2. Dapatkan Bot Token

1. Chat dengan [@BotFather](https://t.me/BotFather) di Telegram
2. Kirim `/newbot` dan ikuti instruksi
3. Copy token bot yang diberikan

### 3. Dapatkan API ID dan API Hash

1. Kunjungi [https://my.telegram.org](https://my.telegram.org)
2. Login dengan nomor Telegram Anda
3. Klik "API development tools"
4. Buat aplikasi baru dan catat `api_id` dan `api_hash`

### 4. Konfigurasi Bot

**Opsi 1: Menggunakan file config.py (Direkomendasikan)**

1. Copy `config_example.py` ke `config.py`
2. Edit `config.py` dan isi dengan kredensial Anda:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
API_ID = "12345678"
API_HASH = "abcdef1234567890abcdef1234567890"
```

**Opsi 2: Edit langsung main.py**

Edit file `main.py` dan ganti nilai berikut:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
API_ID = "YOUR_API_ID_HERE"
API_HASH = "YOUR_API_HASH_HERE"
```

### 5. Test Koneksi (Opsional)

Sebelum menjalankan bot, Anda bisa test koneksi terlebih dahulu:

```bash
python test_connection.py
```

Script ini akan memverifikasi:
- Bot token valid
- API ID dan API Hash valid
- Koneksi ke Telegram API berhasil

### 6. Jalankan Bot

**Opsi 1: Menggunakan script (Direkomendasikan)**

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```cmd
run.bat
```

**Opsi 2: Manual**
```bash
python main.py
```

### 7. Menjalankan sebagai Service (Linux)

Untuk menjalankan bot sebagai service yang auto-restart:

1. Edit `telegram-bot.service` dan ganti:
   - `YOUR_USERNAME` dengan username Anda
   - `/path/to/telegram-media-downloader` dengan path lengkap ke folder bot

2. Copy service file:
```bash
sudo cp telegram-bot.service /etc/systemd/system/
```

3. Enable dan start service:
```bash
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service
```

4. Cek status:
```bash
sudo systemctl status telegram-bot.service
```

5. Lihat log:
```bash
sudo journalctl -u telegram-bot.service -f
```

## Penggunaan

### YouTube Audio Download

```
/yt https://youtube.com/watch?v=VIDEO_ID
/yt nama lagu
/yt dewa 19 risalah hati
/yt@your_bot_username https://youtube.com/watch?v=VIDEO_ID
```

### Telegram Media Fetch

```
/tg https://t.me/channel_name/123
/tg https://t.me/BIOSKOP_FILM_HOROR_INDONESIAAA/3986
/tg@your_bot_username https://t.me/channel_name/123
```

### Contoh Interaksi

1. **Start bot**: `/start` atau `/help`
2. **Download lagu**: `/yt dewa 19 risalah hati`
3. **Download dari URL**: `/yt https://youtube.com/watch?v=dQw4w9WgXcQ`
4. **Fetch video dari Telegram**: `/tg https://t.me/movie_channel/1234`
5. **Fetch document dari Telegram**: `/tg https://t.me/document_channel/5678`

## Format Link yang Didukung

- **YouTube**: `https://youtube.com/watch?v=...` atau `https://youtu.be/...`
- **Telegram**: `https://t.me/channel_name/message_id`

## Catatan Penting

1. **API Credentials**: Pastikan API ID dan API Hash sudah dikonfigurasi dengan benar
2. **File Size**: Maksimal ukuran file 50MB (batasan Telegram)
3. **Private Channels**: Bot hanya bisa mengakses channel public atau channel yang sudah di-join
4. **Link Copy**: Fitur Telegram hanya bekerja dengan link yang bisa di-copy (tidak bisa di-forward)
5. **YouTube Duration**: Maksimal durasi video YouTube 10 menit
6. **Rate Limiting**: Bot memiliki delay untuk menghindari rate limiting Telegram API

## Batasan

- **File Size**: Maksimal 50MB per file
- **YouTube Duration**: Maksimal 10 menit
- **Channel Access**: Hanya channel public atau yang sudah di-join
- **Media Types**: Video, Audio, Document, Photo
- **Concurrent Downloads**: Satu file per request

## Troubleshooting

### Error "API ID dan API Hash belum dikonfigurasi"
- Pastikan `API_ID` dan `API_HASH` sudah diset di `main.py`
- Pastikan format API ID berupa string angka

### Error "Pesan tidak ditemukan atau channel bersifat private"
- Pastikan channel bersifat public
- Atau bot sudah join ke channel tersebut
- Pastikan link format benar

### Error "File terlalu besar"
- File melebihi batas 50MB Telegram
- Coba dengan file yang lebih kecil

### Error "Video terlalu panjang"
- Video YouTube melebihi batas 10 menit
- Coba dengan video yang lebih pendek

### Error "Gagal mendownload media"
- Channel mungkin private atau bot tidak punya akses
- Pastikan link format benar
- Coba dengan link lain

### Bot tidak merespon
- Pastikan bot token benar
- Cek apakah bot sedang berjalan
- Restart bot jika perlu

### Error "ffmpeg not found"
- Install ffmpeg sesuai instruksi di atas
- Pastikan ffmpeg ada di PATH sistem

## Dependencies

- `aiohttp`: HTTP client untuk Telegram Bot API
- `yt-dlp`: YouTube downloader
- `telethon`: Telegram client library
- `ffmpeg`: Audio converter (harus terinstall di sistem)

## Struktur Proyek

```
telegram-media-downloader/
├── main.py                 # File utama bot
├── config_example.py       # Template konfigurasi
├── requirements.txt        # Dependencies Python
├── README.md              # Dokumentasi
├── CHANGELOG.md           # Riwayat perubahan
├── FEATURES.md            # Overview fitur
├── .gitignore             # File yang diignore git
├── install.sh             # Script instalasi Linux/macOS
├── install.bat            # Script instalasi Windows
├── run.sh                 # Script menjalankan bot Linux/macOS
├── run.bat                # Script menjalankan bot Windows
├── test_connection.py     # Script test koneksi
└── telegram-bot.service   # Systemd service file (Linux)
```

## License

MIT License