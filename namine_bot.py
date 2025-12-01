
import os
import json
import random
from datetime import datetime, timezone, time

import discord
from discord import app_commands
from discord.ext import tasks
import asyncio

# -------------------------------------------------------
# Quotes
# -------------------------------------------------------

NAMINE_BDAY_QUOTES = [
    # Gentle & Heartfelt
    "happy birthday… I hope today feels like a page drawn in light.",
    "even memories fade, but today deserves to stay bright forever.",
    "your heart's story added another beautiful chapter today.",
    "I'm glad you exist — it makes every memory a little warmer.",
    "some birthdays are loud. yours feels like a soft song.",
    "I hope your day feels like it was drawn with sunlight.",
    "every candle holds a wish, and I think yours will come true.",
    "if I could paint this moment, it would glow.",
    "happy birthday. don't forget to make a memory worth keeping.",
    "you've changed so much since I first met your heart.",

    # Memory & Reflection
    "it's strange… even memories celebrate birthdays, in their own way.",
    "when you smile, even forgotten dreams remember their warmth.",
    "do you ever wonder if memories age too? today, they all feel young.",
    "your heart remembers more kindness than you realize.",
    "every year, your story becomes more vivid in my sketches.",
    "even nobodies can feel happy seeing you smile today.",
    "if hearts could whisper, yours would be singing.",
    "you're proof that even fleeting moments can last forever.",
    "I can't draw time, but I can draw how it feels with you.",
    "another year, another reason your light keeps shining in my mind.",

    # Dreamlike & Poetic
    "it's your birthday… the kind of day that feels like a dream I'd never want to forget.",
    "the stars must have stayed up late just to watch you grow older.",
    "you're the kind of memory that paints itself.",
    "the light today feels softer — maybe it's because of you.",
    "the air hums like a melody your heart wrote itself.",
    "today feels like a wish that came true quietly.",
    "if time is a canvas, then this day is your masterpiece.",
    "even the wind slows down to watch you smile today.",
    "sometimes happiness doesn't shout — it sketches softly.",
    "birthdays remind hearts that time is both fleeting and kind.",

    # Softly Emotional
    "you don't need to remember every birthday — just the feeling that you mattered.",
    "you're the reason some of my best drawings smile back.",
    "if I could, I'd give you a sketch filled with all your favorite memories.",
    "you're one of the few things that makes nothingness feel full.",
    "even in silence, the heart celebrates you.",
    "I think your heart hums louder on your birthday.",
    "sometimes, all a heart needs is to be seen — and today, everyone sees you.",
    "the world feels softer around you today.",
    "maybe memories bloom every year on this day.",
    "happy birthday… I hope the day paints itself kindly for you.",

    # Bittersweet & Reflective
    "even if memories fade, I'll draw yours again.",
    "birthdays remind me how fragile and beautiful time can be.",
    "it's okay to outgrow old memories — you're becoming someone new.",
    "every year, I think you shine a little brighter — even if you don't notice.",
    "if you forget this day someday, I'll remember it for you.",
    "even in quiet hearts, birthdays echo softly.",
    "the older you grow, the stronger your light becomes.",
    "maybe hearts grow the same way memories do — quietly.",
    "if I drew today, I'd use colors I've never used before.",
    "you deserve a world that remembers your kindness.",

    # Hopeful & Encouraging
    "your heart still has so many stories left to draw.",
    "every birthday is a reminder — you're still becoming.",
    "your journey's just beginning, even if you've come so far.",
    "every wish you make today will ripple through the worlds.",
    "you're not just aging — you're unfolding.",
    "keep choosing the light, even when the sky feels dim.",
    "your laughter could brighten the darkest corridor.",
    "if I could, I'd draw you surrounded by everything you love.",
    "you deserve peace, even on the loudest birthdays.",
    "every year you grow, your heart finds more to protect.",

    # Friendship & Warmth
    "you've been part of my story longer than you realize.",
    "thank you for letting me exist in your memories.",
    "even if I forget everything else, I'll remember your smile.",
    "you've given me more warmth than most worlds ever could.",
    "I'm glad your story crossed mine.",
    "happy birthday to someone whose heart could light up a sketchbook.",
    "you make remembering worth the effort.",
    "sometimes, I think your heart teaches others how to stay kind.",
    "you're proof that connection makes even the emptiest places bloom.",
    "you remind me that even nobodies can make memories that matter.",

    # Soft Humor & Shyness
    "do birthdays make you nervous too? or is that just me?",
    "I was going to draw your cake, but it melted before I finished.",
    "don't worry, I didn't forget your birthday — I just misplaced the memory.",
    "happy birthday! I hope your candles behave better than Axel's fire did.",
    "if I could bake, I'd make you a cake shaped like your heart — complicated but sweet.",
    "you deserve confetti, not chaos… though maybe a little chaos.",
    "I was going to sing, but I'll stick to drawing instead.",
    "birthdays are weird. you grow older, but you still look like you stepped out of a dream.",
    "I made you a card… but then I drew over it. sorry.",
    "maybe I should've asked Roxas how to celebrate — he'd probably eat the cake first.",

    # Poetic & Meaningful
    "if hearts could give gifts, mine would give you a memory that never fades.",
    "you're a sketch that time refuses to erase.",
    "if today is a song, it sounds like hope.",
    "every birthday you have reminds me that even lost things can grow.",
    "you're not a fleeting moment — you're a memory that anchors others.",
    "the world feels like it's holding its breath just for you.",
    "your light paints the spaces between hearts.",
    "even in silence, I can feel your birthday echo.",
    "you're the art that keeps remaking itself.",
    "happy birthday — from one memory to another.",

    # Gentle Closers
    "I hope this year feels like a sketch filled with joy.",
    "may your heart stay gentle, even as the world changes.",
    "another year, another reason I'm glad you're here.",
    "your story matters, even in the quiet pages.",
    "I hope your dreams remember you tonight.",
    "happy birthday — may your light never blur.",
    "you're the calm between every storm.",
    "if today were a drawing, I'd never finish it — I'd want to stay in it forever.",
    "you deserve to be remembered — not for what you do, but for who you are.",
    "happy birthday. I'll keep this moment safe in my heart, even if I'm only a memory."
]


# -------------------------------------------------------
# JSON Helper Functions
# -------------------------------------------------------

BIRTHDAY_FILE = "birthdays.json"
CONFIG_FILE = "birthday_config.json"
BIRTHDAY_SONG_FILE = "happy_birthday.mp3"



def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# -------------------------------------------------------
# Bot Client
# -------------------------------------------------------

class NamineBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.voice_states = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        daily_check.start()
        print("🌙 Naminé birthday bot is online.")


client = NamineBot()


# -------------------------------------------------------
# Commands
# -------------------------------------------------------

@client.tree.command(
    name="mybirthday",
    description="Set or view your birthday. Use: /mybirthday 07-29"
)
@app_commands.describe(date="Your birthday in MM-DD format.")
async def mybirthday(interaction: discord.Interaction, date: str = None):

    birthdays = load_json(BIRTHDAY_FILE, {})
    user_id = str(interaction.user.id)

    # View mode
    if date is None:
        if user_id not in birthdays:
            await interaction.response.send_message(
                "📘 *Naminé lifts her sketchbook.*\n"
                "I don't have your birthday yet…\n"
                "You can tell me using `/mybirthday 07-29`.",
                ephemeral=True,
            )
            return

        entry = birthdays[user_id]
        await interaction.response.send_message(
            f"💙 I saved your birthday as **{entry['month']:02d}-{entry['day']:02d}**.",
            ephemeral=True,
        )
        return

    # Set mode
    try:
        month, day = map(int, date.split("-"))
        datetime(year=2000, month=month, day=day)
    except:
        await interaction.response.send_message(
            "…Oh. That doesn’t look right.\n"
            "Please use **MM-DD**.",
            ephemeral=True,
        )
        return

    birthdays[user_id] = {"month": month, "day": day}
    save_json(BIRTHDAY_FILE, birthdays)

    await interaction.response.send_message(
        f"📖 *Naminé writes gently.*\n"
        f"Your birthday is now saved as **{month:02d}-{day:02d}**.",
        ephemeral=True,
    )


@client.tree.command(
    name="setuserbirth",
    description="Mod command: set another user's birthday."
)
@app_commands.describe(
    user="The user to update.",
    date="Their birthday in MM-DD format."
)
async def setuserbirth(interaction: discord.Interaction, user: discord.Member, date: str):

    perms = interaction.user.guild_permissions
    if not (perms.manage_guild or perms.manage_messages):
        await interaction.response.send_message(
            "…Only moderators may rewrite someone else's memories.\n"
            "(You need **Manage Server** or **Manage Messages**.)",
            ephemeral=True
        )
        return

    # Validate date
    try:
        month, day = map(int, date.split("-"))
        datetime(year=2000, month=month, day=day)
    except:
        await interaction.response.send_message(
            "That date doesn't look quite right.\n"
            "Please use **MM-DD**, okay?",
            ephemeral=True
        )
        return

    birthdays = load_json(BIRTHDAY_FILE, {})
    birthdays[str(user.id)] = {"month": month, "day": day}
    save_json(BIRTHDAY_FILE, birthdays)

    await interaction.response.send_message(
        f"📖 *Naminé rewrites the memory softly.*\n"
        f"**{user.display_name}**'s birthday is now **{month:02d}-{day:02d}**.",
        ephemeral=False
    )


@client.tree.command(
    name="happybirthday",
    description="Join the tagged user's VC and play a birthday song."
)
@app_commands.describe(user="The birthday person currently in a voice channel.")
async def happybirthday(interaction: discord.Interaction, user: discord.Member):

    # Make sure the file exists on disk
    if not os.path.isfile(BIRTHDAY_SONG_FILE):
        await interaction.response.send_message(
            "📘 *Naminé looks worried.*\n"
            "I can't find the birthday song file on the server…",
            ephemeral=True,
        )
        return

    # Check that the tagged user is in a voice channel
    if not user.voice or not user.voice.channel:
        await interaction.response.send_message(
            f"📘 *Naminé tilts her head.*\n"
            f"**{user.display_name}** isn't in a voice channel right now.",
            ephemeral=True,
        )
        return

    channel = user.voice.channel

    # Let people know what's happening
    await interaction.response.send_message(
        f"🌸 *Naminé quietly joins* {channel.mention} *to play a song for* {user.mention}…",
        ephemeral=False,
    )

    # Try to connect to the voice channel
    try:
        vc = await channel.connect()
    except discord.ClientException:
        # Probably already connected in this guild – reuse that connection
        vc = discord.utils.get(client.voice_clients, guild=interaction.guild)
        if vc is None:
            await interaction.followup.send(
                "…I couldn’t connect to the voice channel.",
                ephemeral=True,
            )
            return

    # Create audio source from the mp3 file
    audio_source = discord.FFmpegPCMAudio(BIRTHDAY_SONG_FILE)

    # Play if not already playing something
    if not vc.is_playing():
        vc.play(audio_source)

    # Wait until the song finishes
    while vc.is_playing():
        await asyncio.sleep(1)

    # Disconnect after playing
    try:
        await vc.disconnect()
    except Exception:
        pass



@client.tree.command(
    name="setbirthdaychannel",
    description="Admin: choose where daily birthday messages go."
)
@app_commands.describe(channel="Channel for birthday announcements.")
async def setbirthdaychannel(interaction: discord.Interaction, channel: discord.TextChannel):

    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(
            "…Only someone who manages this world can choose this.\n"
            "(You need **Manage Server**.)",
            ephemeral=True,
        )
        return

    config = load_json(CONFIG_FILE, {})
    gid = str(interaction.guild.id)

    if gid not in config:
        config[gid] = {}

    config[gid]["channel_id"] = channel.id
    save_json(CONFIG_FILE, config)

    await interaction.response.send_message(
        f"🌙 *Naminé nods softly.*\n"
        f"I'll send birthday wishes in {channel.mention} every afternoon.",
        ephemeral=True,
    )


# -------------------------------------------------------
# Daily Check — 16:00 UTC
# Only posts if it's someone's birthday
# -------------------------------------------------------

@tasks.loop(time=time(hour=16, minute=0, tzinfo=timezone.utc))
async def daily_check():
    print("🔍 Running daily birthday scan…")

    birthdays = load_json(BIRTHDAY_FILE, {})
    config = load_json(CONFIG_FILE, {})
    today = datetime.now(timezone.utc).date()
    m, d = today.month, today.day

    for guild in client.guilds:

        gid = str(guild.id)
        channel_id = config.get(gid, {}).get("channel_id")
        if not channel_id:
            continue

        channel = guild.get_channel(channel_id)
        if channel is None:
            continue

        # Find today's birthdays
        birthday_members = []
        for member in guild.members:
            entry = birthdays.get(str(member.id))
            if entry and entry["month"] == m and entry["day"] == d:
                birthday_members.append(member)

        if not birthday_members:
            continue

        mentions = ", ".join(member.mention for member in birthday_members)
        quote = random.choice(NAMINE_BDAY_QUOTES)

        message = (
            "🌸 **A gentle page turns…**\n"
            "*Naminé has drawn something special today.*\n\n"
            f"💙 Today, {mentions} is celebrating their birthday.\n"
            f"\"{quote}\""
        )

        try:
            await channel.send(message)
        except Exception as e:
            print(f"⚠️ Could not send message in guild {guild.id}: {e}")


# -------------------------------------------------------
# Run Bot
# -------------------------------------------------------

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BIRTH_TOKEN")
    if not TOKEN:
        raise RuntimeError("DISCORD_BIRTH_TOKEN environment variable not set.")
    client.run(TOKEN)
