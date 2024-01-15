from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from utils.database import add_user
from utils.mustjoin import is_user_member
from modules.instagram import download_reel

app = Client("my_bot", bot_token=config.TELEGRAM_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    username = message.from_user.username
    add_user(user_id, username)

    if await is_user_member(client, user_id):
        await message.reply("Welcome to the bot! You're all set to start downloading Instagram Reels.")
    else:
        await message.reply("Please join our channel first to use this bot.",
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("Join Channel", url=f"https://t.me/{config.REQUIRED_CHANNEL.lstrip('@')}")]
                            ]))

@app.on_message(filters.regex(r'https?://www.instagram.com/p/[\w-]+') & ~filters.command)
async def handle_instagram_link(client, message):
    instagram_url = message.matches[0].group(0)
    download_path = await download_reel(instagram_url)

    if download_path:
        await message.reply_video(video=download_path)
    else:
        await message.reply("Sorry, I couldn't download the Reel.")


app.run()
