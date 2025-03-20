import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
TOKEN = os.getenv("7912486606:AAHA0WPAaxeeVgiZHWM0MyOZ4QAY8d3wGb4")
TMDB_API_KEY = os.getenv("9f889c12b65dc684db1c898733fd1477")
CHAT_ID = os.getenv("@P_ete_rbot")  # Your Telegram Chat ID

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

# Fetch trending movies
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    movies = data.get("results", [])[:5]  # Get top 5 trending movies
    return movies

# Send daily trending movies
async def send_daily_updates():
    movies = get_trending_movies()
    if not movies:
        await bot.send_message(CHAT_ID, "Couldn't fetch trending movies today. Try again later.")
        return

    response_text = "**Spooderman here !
🔥 Trending Movies Today:**\n\n"
    for movie in movies:
        title = movie["title"]
        release_date = movie["release_date"]
        rating = movie["vote_average"]
        response_text += f"🎬 {title} ({release_date}) - ⭐ {rating}/10\n"

    await bot.send_message(CHAT_ID, response_text, parse_mode="Markdown")

# Start command
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("This bot sends daily trending movie updates! Stay tuned. 🎥")

# Start scheduler on bot startup
async def on_startup(_):
    scheduler.add_job(send_daily_updates, "cron", hour=10, minute=0)  # Sends updates at 10:00 AM UTC daily
    scheduler.start()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
