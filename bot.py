import os
import requests
import discord
from discord import app_commands
from discord.ext import tasks, commands
import random
from datetime import datetime
import asyncio

# === Demyx The Jokester Jokes ===
KH_MUSIC_JOKES = [
    "Why did Xemnas start a band? Because he wanted to be the *Nobody* who finally got some fans.",
    "Why did Axel refuse to play guitar? He kept burning through the strings.",
    "Why did Roxas quit drumming? Too many broken hearts — and drumsticks.",
    "How many Organization XIII members does it take to change a light bulb? None — they prefer the darkness.",
    "Why did Sora get kicked out of the orchestra? He kept trying to conduct with the Keyblade.",
    "Why is Zexion bad at karaoke? He reads the lyrics like they’re a research report.",
    "Why did Demyx refuse to fight Heartless? He said, 'I only play *soft rock*, not hard mode.'",
    "Why did Kairi join a band? She wanted to find her lost chords.",
    "Why did Goofy start a jazz trio? Because he already mastered the Goof-step.",
    "What’s Xigbar’s favorite song? 'Shot Through the Heart.'",
]

# === Demyx's Roasts ===
DEMYX_ROASTS = [
    "Bro, you’ve got less rhythm than a Heartless on roller skates.",
    "You call that an idea? Even my sitar’s got better thoughts.",
    "I’d explain it to you, but I only have one brain cell left — and it’s busy tuning my strings.",
    "You’re the human equivalent of a background NPC in Twilight Town.",
    "I’ve seen Shadows that cast a brighter light than you.",
    "Did you trip over your own Keyblade again? Classic.",
    "You’d lose a staring contest with a Nobody.",
    "You’re like a B-tier minigame: confusing, pointless, and unskippable.",
    "If laziness were an art, you’d be my magnum opus.",
    "You’d make a great band member — if the band was called 'Off Key'."
]

# === CONFIG ===
CHANNEL_ID = 1423535719648989235

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
    print("🌐 Slash commands synced globally!")

@tasks.loop(minutes=1)
async def post_joke_of_day():
    now = datetime.now()
    if now.hour == 9 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        joke = fetch_joke()
        emote = random.choice(JOKE_EMOTES)
        if channel:
            await channel.send(f"😂 **Joke of the Day** 😂\n{joke}\n{emote}")

@tree.command(name="joke", description="Demyx tells a joke trying to be funny")
async def joke(interaction: discord.Interaction):
    joke_text = fetch_joke()
    emote = random.choice(JOKE_EMOTES)
    await interaction.response.send_message(f"😂 **Random Joke** 😂\n{joke_text}\n{emote}")

@tree.command(name="roast", description="Demyx roasts someone brutally 🔥")
@app_commands.describe(user="Mention the user you want Demyx to roast")
async def roast(interaction: discord.Interaction, user: discord.Member = None):
    target = user.mention if user else interaction.user.mention
    if random.randint(1, 20) == 1:
        self_roasts = [
            "Guess what? I just insulted myself in tune. That’s talent, baby!",
            "Wow... I can’t believe I said that out loud. My therapist’s gonna love this one.",
            "Dang, I just burned myself harder than Axel ever could.",
            "You know you’ve hit rock bottom when your own jokes start hurting you.",
            "...Okay, that one actually stung a bit. Even for me."
        ]
        roast_line = random.choice(self_roasts)
        await interaction.response.send_message(f":DemyxRoast: *Demyx winces mid-strum.*\n{roast_line}")
        return

    roast_line = random.choice(DEMYX_ROASTS)
    await interaction.response.send_message(
        f":DemyxRoast: *Demyx smirks and strums his sitar...*\n{target}, {roast_line}"
    )

@tree.command(name="fadeout", description="Demyx clears the chat — like a melody fading away.")
@app_commands.describe(amount="How many recent messages to fade out (default: 10).")
@commands.has_permissions(manage_messages=True)
async def fadeout(interaction: discord.Interaction, amount: int = 10):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "🎸 *Demyx strums lazily.* 'Whoa there, rockstar. Only the band leaders get to fade the crowd out.'",
            ephemeral=True
        )
        return

    try:
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(
            f"🎶 *Demyx grins.* 'And just like that... {amount} messages fade into silence.'",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"⚠️ *Demyx winces.* 'Something went flat — I couldn’t fade those out.'\n`{e}`",
            ephemeral=True
        )

@tree.command(name="soundcheck", description="Demyx does a soundcheck... eventually.")
async def soundcheck(interaction: discord.Interaction):
    demyx_bits = [
        "🎶 You ever notice how everyone’s always fighting and I’m just—vibing? Yeah. That’s balance, baby.",
        "💧 Is it really procrastination if I *intend* to do it later? Thought so.",
        "🎸 What’s the secret to sounding good? Easy — just play loud enough that nobody can tell you missed a note.",
        "😴 Why rehearse when you can just *feel* the music? …Or nap. Napping works too.",
        "🎤 Who needs a heart when you’ve got rhythm? Well, okay, hearts are nice too, but rhythm’s less dramatic."
    ]
    if random.randint(1, 5) == 1:
        excuses = [
            "😴 Ehh, you know what? Not today. The vibes aren’t aligned.",
            "💤 Soundcheck canceled — my inspiration just… evaporated."
        ]
        await interaction.response.send_message(random.choice(excuses))
        return

    opener = random.choice([
        "🎤 Alright, alright… let’s get this soundcheck rolling!",
        "🎶 Testing, testing... okay, yeah, still awesome."
    ])
    lines = random.sample(demyx_bits, k=3)
    await interaction.response.send_message(f"{opener}\n\n" + "\n".join(lines))

@tree.command(name="setlist", description="🎸 Demyx shows off his full command setlist!")
async def setlist(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎵 Demyx’s Setlist 🎵",
        description="Here’s what Demyx can do when he’s *in the groove!*",
        color=discord.Color.teal()
    )
    embed.add_field(name="😂 /joke", value="Tells a random joke — funny or not!", inline=False)
    embed.add_field(name="🔥 /roast", value="Roasts you or someone else brutally.", inline=False)
    embed.add_field(name="💨 /fadeout", value="Mods only — clears recent messages.", inline=False)
    embed.add_field(name="🎸 /soundcheck", value="Demyx rambles about music and vibes.", inline=False)
    embed.add_field(name="🏓 /ping", value="Check if Demyx is alive and vibing.", inline=False)
    embed.add_field(name="📅 Bonus:", value="Posts a new joke every morning at **9 AM sharp!** ☀️", inline=False)
    embed.set_footer(text="💧 Stay hydrated, stay lazy — Demyx out!")
    await interaction.response.send_message(embed=embed)

@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Dance Watah Dance")

if __name__ == "__main__":
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not DISCORD_TOKEN:
        print("Missing DISCORD_TOKEN environment variable.")
    else:
        bot.run(DISCORD_TOKEN)
