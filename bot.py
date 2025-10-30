import os
DISCORD_TOKEN = os.getenv("DISCORD_JOKE_TOKEN")
import discord
from discord import app_commands
from discord.ext import tasks
import requests
import random
from datetime import datetime
# === CONFIGURE THESE ===
CHANNEL_ID = 1423535719648989235  # replace with your channel ID

# === Emotes to rotate ===
JOKE_EMOTES = [
    "<:custom1:972202193576919110>",
    "<:custom2:1406509489506750534>"
]

# === Discord Setup ===
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

def fetch_joke() -> str:
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=racist"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data["type"] == "single":
                return data["joke"]
            elif data["type"] == "twopart":
                return f"{data['setup']}\n{data['delivery']}"
    except Exception as e:
        print(f"Error fetching joke: {e}")
    return "Couldn't fetch a joke this time 😅"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    post_joke_of_day.start()
    await tree.sync()
    print("🌐 Slash commands synced!")

@tasks.loop(minutes=1)
async def post_joke_of_day():
    now = datetime.now()
    if now.hour == 14 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        joke = fetch_joke()
        emote = random.choice(JOKE_EMOTES)
        if channel:
            await channel.send(f"😂 **Joke of the Day** 😂\n{joke}\n{emote}")

@tree.command(name="joke", description="Get a random joke (no racist jokes)")
async def joke(interaction: discord.Interaction):
    joke_text = fetch_joke()
    emote = random.choice(JOKE_EMOTES)
    await interaction.response.send_message(f"😂 **Random Joke** 😂\n{joke_text}\n{emote}")

@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

if __name__ == "__main__":
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not DISCORD_TOKEN:
        print("Missing DISCORD_TOKEN environment variable.")
    else:
        bot.run(DISCORD_TOKEN)



