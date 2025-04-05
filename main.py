import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import re

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")  # Your RapidAPI Key

bot = Client("insta_reel_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def extract_shortcode(text):
    match = re.search(r"reel/([A-Za-z0-9_-]+)", text)  # Fixed regex
    if match:
        print(f"Extracted Shortcode: {match.group(1)}")  # Debugging line
        return match.group(1)
    return None

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("Send me any Instagram reel link, I'll download it for you!")

@bot.on_message(filters.text & ~filters.command("start"))
async def download_reel(_, message: Message):
    url = message.text
    shortcode = extract_shortcode(url)
    
    if not shortcode:
        return await message.reply_text("Please send a valid Instagram reel link.")

    msg = await message.reply_text("Fetching reel...")

    try:
        # API request
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "instagram230.p.rapidapi.com"
        }

        response = requests.get(
            f"https://instagram230.p.rapidapi.com/post/info?shortcode={shortcode}",
            headers=headers
        )

        json_data = response.json()
        print(json_data)  # Debugging

        video_url = json_data.get("video_url")
        caption = json_data.get("caption", "Instagram Reel")

        if video_url:
            await message.reply_video(video_url, caption=caption)
        else:
            await message.reply_text("Failed to fetch reel. Maybe it's private or API issue.")

    except Exception as e:
        await message.reply_text("Error fetching reel. Check logs.")
        print(f"Error: {e}")
    finally:
        await msg.delete()

bot.run()
