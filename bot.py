import os
import requests
import zipfile
import io
import discord
from discord import app_commands, FFmpegPCMAudio
from discord.ext import tasks, commands
import random
from datetime import datetime
import asyncio

FFMPEG_PATH = os.path.join("bin", "ffmpeg.exe")

def ensure_ffmpeg():
    """Download ffmpeg.exe automatically if it's missing (for Windows use)."""
    if os.name == "nt" and not os.path.exists(FFMPEG_PATH):
        print("🎧 Downloading FFmpeg (first-time setup)...")
        os.makedirs("bin", exist_ok=True)
       url = "https://github.com/eugeneware/ffmpeg-static/releases/download/b5.0.1/ffmpeg-win64-v5.0.1.zip"
        r = requests.get(url, timeout=60)
        if r.status_code != 200:
            print("⚠️ Failed to download FFmpeg!")
            return
        z = zipfile.ZipFile(io.BytesIO(r.content))
        exe_path = None
        for name in z.namelist():
            if name.endswith("ffmpeg.exe"):
                exe_path = name
                break
        if exe_path:
            z.extract(exe_path, "bin")
            new_path = os.path.join("bin", "ffmpeg.exe")
            os.rename(os.path.join("bin", exe_path), new_path)
            print("✅ FFmpeg ready at:", new_path)
        else:
            print("⚠️ Could not find ffmpeg.exe inside the ZIP file.")
    else:
        print("✅ FFmpeg already available or not required on this OS.")

ensure_ffmpeg()
# === Demyx The Jokester Jokes ===
KH_MUSIC_JOKES = [
    # Kingdom Hearts jokes
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
    "Why did Ansem hate rhythm games? He couldn’t handle the beat of darkness.",
    "Why does Marluxia only listen to vinyl? Because he says petals sound warmer that way.",
    "Why did Larxene get kicked out of the band? Too much shocking stage presence.",
    "Why did Luxord bring cards to the concert? He was ready to deal with the fans.",
    "What do you call Demyx’s new album? *Water You Waiting For?*",
    "Why did Saïx never finish his song? He always howled before the chorus.",
    "What’s Xion’s favorite genre? Covers.",
    "Why did Riku start a rock band? To finally play something light *and* dark.",
    "Why is Sora’s singing always on key? Because he has a *Keyblade.*",
    "Why doesn’t Donald play guitar? Because every solo ends in a quack-up.",
    # Music jokes
    "Why did the drummer go to jail? He got caught beating it.",
    "What do you call a musician with no girlfriend? Homeless.",
    "Why did the bassist break up with the keyboardist? Too many treble issues.",
    "Why did the music teacher go to jail? For fingering A minor.",
    "Why did the microphone file a complaint? It was being talked over.",
    "Why don’t guitarists get along? They’re always stringing each other along.",
    "Why did the note go to school? To get a little sharp.",
    "Why did Mozart hate chickens? Because they kept saying 'Bach, Bach, Bach!'",
    "Why did the piano break up with the saxophone? It couldn’t handle the jazz.",
    "Why did the concert end early? The crowd couldn’t handle the bass drop.",
    "Why did the metronome get promoted? It always kept time.",
    "Why did Beethoven get rid of his chickens? They kept saying 'Bach!'",
    "Why did the DJ get in trouble? He dropped the wrong beat.",
    "Why was the music book sad? It had too many notes.",
    "Why did the singer bring a ladder? To reach the high notes.",
    "Why do musicians make terrible detectives? They always follow the wrong leads.",
    "Why did the note get detention? It was too flat.",
    "Why did the guitarist cross the road? To get to the next gig.",
    "What’s a skeleton’s favorite instrument? The trom-bone.",
    "Why did the singer lose his voice? He couldn’t handle the mic-drop.",
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
    "You’d make a great band member — if the band was called 'Off Key'.",
    "Your sense of humor’s as dry as Agrabah.",
    "If brains were munny, you’d still owe the Moogle.",
    "You remind me of a Gummi Ship — slow, loud, and built wrong.",
    "You look like someone pressed randomize on a character creator and just said 'good enough.'",
    "Even Xigbar’s aim is better than your life choices.",
    "If cringe was darkness, you’d be the new Ansem.",
    "You’ve got the energy of a D-ranked mission.",
    "You’d lose a fight against a tutorial enemy.",
    "Are you sure you’re not part Heartless? Because you’ve got zero soul and too much noise.",
    "I’d call you a vibe killer, but that would imply you had a vibe to begin with."
]
DEMYX_ROASTS += [
    "You're like a loading screen tip — no one reads you and you take too long to show up.",
    "Even Donald’s magic hits harder than your comebacks.",
    "You’ve got less depth than Atlantica’s swimming controls.",
    "If confusion were power, you’d be the next Keyblade Master.",
    "You make Organization XIII look like a comedy troupe.",
    "You couldn’t organize a save file, let alone a mission.",
    "You’ve got the enthusiasm of a Shadow Heartless at a pep rally.",
    "You remind me of a synth panel — loud noises, zero results.",
    "You’d probably get lost in Traverse Town’s tutorial section.",
    "Your existence is the emotional equivalent of low battery mode.",
    "If Roxas had two brain cells, you’d still be missing one.",
    "You look like a failed fusion between Goofy and a memory fragment.",
    "Even the Moogles charge extra to deal with you.",
    "You’d trip over your own sitar strings trying to look cool.",
    "If sarcasm were XP, I’d level up every time you talk.",
    "You’ve got less presence than a Nobody at a birthday party.",
    "You make Atlantica’s rhythm minigame look like a masterpiece.",
    "Even Xaldin’s wind listens better than you do.",
    "You’ve got more plot holes than Kingdom Hearts’ timeline.",
    "If failure were currency, you’d own all of Twilight Town.",
    "You could fall asleep during your own roast — and still lose.",
    "You’re like a Gummi Ship — somehow both clunky and fragile.",
    "I’ve seen Dusk Nobodies with more rhythm than you.",
    "You’ve got the personality of an unskippable cutscene.",
    "Your sense of timing makes Luxord cry.",
    "You’d probably lose a staring contest with Roxas’s blank expression.",
    "You bring less energy than a drained Drive Gauge.",
    "You’re proof that respawning doesn’t fix mistakes.",
    "You look like you failed a charisma check in real life.",
    "You’ve got more lag than Atlantica’s singing segments.",
    "If being awkward were a skill, you’d be S-rank.",
    "You’re like Larxene’s lightning — all noise, no precision.",
    "You’d forget your own roast halfway through it.",
    "You’ve got the same vibe as an out-of-tune boss theme.",
    "You could stand next to Xemnas and still be the least intimidating one there.",
    "Even the Heartless ignore you out of pity.",
    "You’ve got less emotional range than a locked cutscene camera.",
    "You make background NPCs look ambitious.",
    "You’d get lost walking from one world to the next — with a map.",
    "You’ve got 'side quest energy' written all over you.",
    "You talk like you skipped half your own dialogue options.",
    "If effort were XP, you’d still be level one.",
    "You’d make a great background noise — if silence wasn’t better.",
    "Even Vexen’s experiments have more life than your social skills.",
    "You’re like a Keyblade without a wielder — pointless and flashy.",
    "You’ve got less soul than a Nobody cover band.",
    "If cringe could open Kingdom Hearts, you’d be the chosen one.",
    "You’d forget your own joke setup mid-sentence.",
    "Even Demyx thinks you’re too lazy — and that’s saying something.",
    "You’ve got the comedic timing of a frozen synth wave.",
    "You’d be a perfect Nobody — no purpose, no direction, just vibes."
]

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
    await tree.sync(guild=None)  # Sync globally
    print("🌐 Slash commands synced globally!")

@tasks.loop(minutes=1)
async def post_joke_of_day():
    now = datetime.now()
    if now.hour == 14 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        joke = fetch_joke()
        emote = random.choice(JOKE_EMOTES)
        if channel:
            await channel.send(f"😂 **Joke of the Day** 😂\n{joke}\n{emote}")

@tree.command(name="play", description="Demyx joins your VC and plays a random sound!")
async def play(interaction: discord.Interaction):
    user = interaction.user

    if not user.voice or not user.voice.channel:
        await interaction.response.send_message(
            "🎸 *Demyx strums his sitar lazily.* 'Uh... maybe join a voice channel first, yeah?'"
        )
        return

    voice_channel = user.voice.channel
    sound_dir = "sounds"
    supported_formats = (".mp3", ".wav", ".ogg")

    if not os.path.exists(sound_dir):
        await interaction.response.send_message(
            "🎶 *Demyx looks around.* 'Uh, my sound folder’s missing, man!'"
        )
        return

    sound_files = [f for f in os.listdir(sound_dir) if f.endswith(supported_formats)]
    if not sound_files:
        await interaction.response.send_message(
            "🎸 *Demyx shrugs.* 'No tracks to jam with, dude!'"
        )
        return

    sound_file = random.choice(sound_files)
    sound_path = os.path.join(sound_dir, sound_file)

    try:
        vc = await voice_channel.connect()
        await interaction.response.send_message(
            f"🎶 *Demyx pops into {voice_channel.name}.* 'Let’s jam!' 🎵 Now playing: `{sound_file}`"
        )

        # Make sure FFmpeg is detected
        if not os.path.exists("bin/ffmpeg.exe") and os.name == "nt":
            print("⚠️ FFmpeg not found — attempting to use system installation.")

        source = FFmpegPCMAudio(sound_path)
        vc.play(source)
        print(f"🎵 Started playing: {sound_path}")

        while vc.is_playing():
            await asyncio.sleep(1)

        print("✅ Finished playing, disconnecting...")
        await vc.disconnect()
        await interaction.followup.send(
            "🎤 *Demyx waves.* 'Okay, okay, that’s enough music for now!'"
        )

    except Exception as e:
        print(f"⚠️ Playback error: {e}")
        await interaction.response.send_message(
            f"⚠️ *Demyx scratches his head.* 'Something went wrong playing the sound. ({e})'"
        )


@tree.command(name="joke", description="Demyx tells a joke trying to be funny")
async def joke(interaction: discord.Interaction):
    joke_text = fetch_joke()
    emote = random.choice(JOKE_EMOTES)
    await interaction.response.send_message(f"😂 **Random Joke** 😂\n{joke_text}\n{emote}")

@tree.command(name="roast", description="Demyx roasts someone brutally 🔥")
@app_commands.describe(user="Mention the user you want Demyx to roast")
async def roast(interaction: discord.Interaction, user: discord.Member = None):
    target = user.mention if user else interaction.user.mention

    # 5% chance that Demyx roasts himself instead
    if random.randint(1, 20) == 1:
        self_roasts = [
            "Guess what? I just insulted myself in tune. That’s talent, baby!",
            "Wow... I can’t believe I said that out loud. My therapist’s gonna love this one.",
            "Dang, I just burned myself harder than Axel ever could.",
            "You know you’ve hit rock bottom when your own jokes start hurting you.",
            "...Okay, that one actually stung a bit. Even for me."
        ]
        roast_line = random.choice(self_roasts)
        await interaction.response.send_message(
            f":DemyxRoast: *Demyx winces mid-strum.*\n{roast_line}"
        )
        return

    # Normal roast with mention
    roast_line = random.choice(DEMYX_ROASTS)
    await interaction.response.send_message(
        f":DemyxRoast: *Demyx smirks and strums his sitar...*\n{target}, {roast_line}"
    )


@tree.command(name="fadeout", description="Demyx clears the chat — like a melody fading away.")
@app_commands.describe(amount="How many recent messages to fade out (default: 10).")
@commands.has_permissions(manage_messages=True)
async def fadeout(interaction: discord.Interaction, amount: int = 10):
    """Deletes a specified number of recent messages — admin/mod only."""
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("🎸 *Demyx strums lazily.* 'Whoa there, rockstar. Only the band leaders get to fade the crowd out.'", ephemeral=True)
        return

    try:
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(f"🎶 *Demyx grins.* 'And just like that... {amount} messages fade into silence.'", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"⚠️ *Demyx winces.* 'Something went flat — I couldn’t fade those out.'\n`{e}`", ephemeral=True)   

@tree.command(name="soundcheck", description="Demyx does a soundcheck... eventually.")
async def soundcheck(interaction: discord.Interaction):
    # Demyx's self-answering "trivia" rants
    demyx_bits = [
        "🎶 You ever notice how everyone’s always fighting and I’m just—vibing? Yeah. That’s balance, baby.",
        "💧 Is it really procrastination if I *intend* to do it later? Thought so.",
        "🎸 What’s the secret to sounding good? Easy — just play loud enough that nobody can tell you missed a note.",
        "😴 Why rehearse when you can just *feel* the music? …Or nap. Napping works too.",
        "🎤 Who needs a heart when you’ve got rhythm? Well, okay, hearts are nice too, but rhythm’s less dramatic.",
        "🎵 You ever think about how water has no shape, but still *flows*? Kinda like my work ethic.",
        "💦 What’s my warmup routine? Oh, you mean pretending to tune the sitar while stalling? Classic.",
        "🎶 Why fight Heartless when you can drown them in good vibes? Oh wait—Xemnas said that’s not ‘productive.’",
        "🎸 You know, some people train for years to master their craft. Me? I wing it and hope the audience’s standards are low.",
        "🎤 Do I take requests? Yeah — requests to stop talking, usually.",
        "🎵 Ever try to play a song underwater? Don’t. Just trust me on that one.",
        "💧 They say ‘music heals the heart.’ Cool, guess I’m a doctor now!",
        "🎶 Every day’s a performance, right? Mine just has… fewer people clapping.",
        "🎸 Can’t spell ‘melodious’ without ‘me.’ Well, you can, but it’s not as fun.",
        "🎤 I asked Xigbar to be my hype man once. He said I needed fans first. Rude."
    ]

    banter_openers = [
        "🎤 Alright, alright… let’s get this soundcheck rolling!",
        "🎶 Testing, testing... okay, yeah, still awesome.",
        "💦 Is this thing on? Oh, right, it’s *me* — so yeah, obviously it is.",
        "🎸 Time for another world-class performance nobody asked for!",
        "😎 Ladies, gents, and Nobodies — Demyx in the house!"
    ]

    lazy_excuses = [
        "😴 Ehh, you know what? Not today. The vibes aren’t aligned.",
        "💤 Soundcheck canceled — my inspiration just… evaporated.",
        "💧 Sorry, can’t. My sitar’s emotionally unavailable right now.",
        "🎸 Soundcheck? Nah, too mainstream.",
        "🙃 Let’s skip it. I’m on my break. Again.",
        "😪 I'm too tired for you, ask me when I feel like answering.\n*...which could be never 😴*"
    ]

    # 1-in-5 chance Demyx refuses to do anything
    if random.randint(1, 5) == 1:
        excuse = random.choice(lazy_excuses)
        await interaction.response.send_message(excuse)
        return

    opener = random.choice(banter_openers)
    lines = random.sample(demyx_bits, k=3)
    performance = f"{opener}\n\n" + "\n".join(lines) + "\n\n🎶 Soundcheck complete — nailed it (probably)."
    await interaction.response.send_message(performance)


@tree.command(name="setlist", description="🎸 Demyx shows off his full command setlist!")
async def setlist(interaction: discord.Interaction):
    """Displays all available Demyx commands in a fun, musical format."""
    embed = discord.Embed(
        title="🎵 Demyx’s Setlist 🎵",
        description="Here’s what Demyx can do when he’s *in the groove!*",
        color=discord.Color.teal()  # Aqua/turquoise theme for Demyx
    )

    embed.add_field(
        name="🎶 /play",
        value="Demyx joins your voice channel and plays a random soundboard clip.",
        inline=False
    )
    embed.add_field(
        name="😂 /joke",
        value="Demyx tells a random joke — whether it’s funny or not is debatable.",
        inline=False
    )
    embed.add_field(
        name="🔥 /roast",
        value="Demyx roasts you or a tagged user mercilessly. 5% chance he roasts himself instead.",
        inline=False
    )
    embed.add_field(
        name="💨 /fadeout",
        value="Moderators only — clears a number of recent messages, like a melody fading away.",
        inline=False
    )
    embed.add_field(
        name="🎸 /soundcheck",
        value="Demyx rambles through his random music-flavored wisdom.",
        inline=False
    )
    embed.add_field(
        name="🏓 /ping",
        value="Check if Demyx is alive and jamming.",
        inline=False
    )

    embed.add_field(
        name="📅 Bonus:",
        value="Demyx also posts a new joke every morning at **9 AM sharp!** ☀️",
        inline=False
    )

    embed.set_footer(text="💧 Stay hydrated, stay lazy — Demyx out!")
    await interaction.response.send_message(embed=embed)


@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Dance Watah Dance")


if __name__ == "__main__":
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not DISCORD_TOKEN:
        print("Missing DISCORD_JOKE_TOKEN environment variable.")
    else:
        bot.run(DISCORD_TOKEN)

        

















