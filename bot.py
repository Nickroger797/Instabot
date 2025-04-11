import os
import re
import instaloader
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from script import start_text, about_text, help_text

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("insta_reel_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Instaloader setup
loader = instaloader.Instaloader(
    save_metadata=False,
    download_comments=False,
    post_metadata_txt_pattern=''
)
# Load saved session (you must login once using instaloader CLI)
loader.load_session_from_file("your_username")  # replace with your IG username

def extract_shortcode(link):
    match = re.search(r"instagram\.com/reel/([^/?\s]+)", link)
    return match.group(1) if match else None

def extract_username(text):
    match = re.search(r"instagram\.com/([^/?\s]+)", text)
    return match.group(1) if match else text.replace("@", "").strip()

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Join Update Channel", url="https://t.me/yourchannel")],
            [
                InlineKeyboardButton("ℹ️ Help", callback_data="help"),
                InlineKeyboardButton("💡 About", callback_data="about"),
                InlineKeyboardButton("👤 Owner", url="https://t.me/yourusername")
            ]
        ]
    )
    await message.reply_text(start_text, reply_markup=buttons)

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data

    if data == "about":
        await callback_query.message.edit_text(about_text, reply_markup=callback_query.message.reply_markup)
    elif data == "help":
        await callback_query.message.edit_text(help_text, reply_markup=callback_query.message.reply_markup)

@bot.on_message(filters.text & ~filters.command(["start"]))
async def reel_downloader(_, message: Message):
    text = message.text.strip()

    # Single reel URL
    if "instagram.com/reel/" in text:
        shortcode = extract_shortcode(text)
        if not shortcode:
            return await message.reply_text("❌ Invalid Instagram Reel URL.")
        
        msg = await message.reply_text("⏳ Downloading reel...")
        try:
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            video_url = post.video_url
            await message.reply_video(video=video_url, caption=post.caption or "Instagram Reel")
        except Exception as e:
            print("Error:", e)
            await message.reply_text("⚠️ Failed to fetch reel. Make sure it's *public*.")
        await msg.delete()
    
    # Username bulk download
    elif "instagram.com/" in text or text.startswith("@") or len(text) < 30:
        username = extract_username(text)
        msg = await message.reply_text(f"⏳ Fetching reels of `{username}`...")

        try:
            profile = instaloader.Profile.from_username(loader.context, username)
            count = 0

            for post in profile.get_posts():
                if post.typename == "GraphVideo":
                    await message.reply_video(video=post.video_url, caption=post.caption or "Instagram Reel")
                    count += 1
                    if count >= 5:  # Limit to 5 reels max
                        break

            if count == 0:
                await message.reply_text("❌ No reels found.")
            else:
                await msg.edit(f"✅ Sent {count} reel(s) from `{username}`.")

        except Exception as e:
            print("Error:", e)
            await msg.edit("⚠️ Failed to fetch reels. Make sure the profile is *public*.")

    else:
        await message.reply_text("❌ Send a valid Instagram reel link or username.")

bot.run()
