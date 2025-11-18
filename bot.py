import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# ==========================================
# ⬇️ عمر المعلومات ديالك هنا ⬇️
# ==========================================
my_api_id = 33162207  # الرقم ديالك
my_api_hash = "28ae35afb00cd5fd3fc5be77d51f68ea"
my_bot_token = "8255625977:AAE88uHkRkpc531mQ3IjYdrm7Speqdpyh6Y"
# ==========================================

app = Client(
    "video_downloader",
    api_id=my_api_id,
    api_hash=my_api_hash,
    bot_token=my_bot_token
)

def download_video_from_url(url):
    ydl_opts = {
        'format': 'best',  # ✅ هاد التعديل غايحل المشكل ديال ffmpeg
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict)
        return file_path, info_dict.get('title', 'Video')

@app.on_message(filters.text & filters.private)
async def handle_url(client, message):
    url = message.text

    if not url.startswith(("http://", "https://")):
        await message.reply("⚠️ عفاك صيفط ليا رابط (Lien) صحيح.")
        return

    status_msg = await message.reply("⏳  كنتيليشارجي الفيديو دابا...")

    try:
        file_path, title = download_video_from_url(url)
        
        await status_msg.edit("⬆️ جاري الإرسال...")

        await message.reply_video(
            video=file_path,
            caption=f"🎬 **{title}**",
            supports_streaming=True
        )

        if os.path.exists(file_path):
            os.remove(file_path)
        
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit(f"❌ وقع خطأ: {str(e)}")

print("🤖 البوت خدام بلا مشاكل! (ديماري)")
app.run()