import os
DISCORD_TOKEN = os.getenv("DISCORD_WORD_TOKEN")
WORDNIK_API_KEY = os.getenv("WORDNIK_API_KEY")

CHANNEL_ID = 1372420087268773979
import discord
from discord import app_commands  # ✅ correct import
from discord.ext import tasks  # ✅ for background loops
import requests
import re
from datetime import datetime

  
# === Discord Setup ===
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
# --- Clean Wordnik HTML/markup ---
def clean_definition(text: str) -> str:
    """Remove HTML tags and Wordnik markup."""
    cleaned = re.sub(r"<.*?>", "", text)  # remove <...> tags
    return cleaned.strip()

# --- Fetch Word of the Day from Wordnik ---
def fetch_word_of_the_day():
    """Fetch the official Word of the Day from Wordnik API."""
    url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay"
    params = {"api_key": WORDNIK_API_KEY}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            word = data.get("word", "Unknown")
            definitions = data.get("definitions", [])
            if definitions:
                raw_def = definitions[0].get("text", "No definition available.")
                return word, clean_definition(raw_def)
            return word, "No definition available."
    except Exception as e:
        print(f"Error fetching Word of the Day: {e}")
    return "Error", "Could not fetch Word of the Day."

# --- Events ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await tree.sync()  # 👈 this tells Discord to register your slash commands
    print("🌐 Slash commands synced.")

# --- Scheduled WOTD (9:00 AM) ---
@tasks.loop(minutes=1)
async def post_word_of_day():
    """Post Word of the Day at 9:00 AM server time."""
    now = datetime.now()
    if now.hour == 14 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        word, definition = fetch_word_of_the_day()
        await channel.send(f"📚 **Word of the Day**: **{word}**\n{definition}")

# --- Slash Commands ---
@tree.command(name="ping", description="Check if the bot is online 🏓")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

@tree.command(name="wotd", description="Get today's Word of the Day 📚")
async def wotd(interaction: discord.Interaction):
    word, definition = fetch_word_of_the_day()
    await interaction.response.send_message(f"📚 **Word of the Day**: **{word}**\n{definition}")


# === Run Bot ===
bot.run(DISCORD_TOKEN)







