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
     "What is Aqua and Ven’s favorite ride at Disney World? The Tower of Terra!",
    "How come Master Xehanort was arrested? They got him on possession!",
    "How come Sora didn’t want to go on an almond diet? Because that’s just nuts…",
    "What is Jiminy Cricket’s least favorite song? No more bugs!!",
    "How come everyone loves Aqua so much? Cuz she’s got a bubbly personality!",
    "What kind of music does Donald like listening to on Halloween? Wrap music!",
    "What is HalloweenTown Sora’s favorite fruit? Neck-tarines!",
    "Who is Pac-man’s favorite Kingdom Hearts character? Wakka Wakka Wakka!!",
    "What is Xemnas’s favorite Thanksgiving food? NOTHING – he’s already stuffed!",
    "Which Kingdom Hearts song is safe for pool diving? The Deep End!",
    "What do you get when you cross Christmastown Donald with Halloweentown Sora? Frostbite.",
    "What is Monstro’s favorite game show? Whale of Fortune!",
    "How come Hades had to start turning people away from the Underworld? Cuz it’s already so crowded. Everyone’s just dying to get in!",
    "Why don’t shadow heartless need cable to watch TV? Cuz they already have their own antennas!",
    "What did Namine say to her Valentine? I love you with all my art!",
    "What’s the most tedious part of BBS? Command Bored!",
    "Why did Tron and Data Sora decide to become friends? They just clicked!",
    "What do all of the KH characters think of Lingering Will? He’s very cape-able!",
    "How does Marluxia make munny? By petaling goods.",
    "Did you hear the joke about the unstamped postcard from Traverse Town? Never mind, you won’t get it…",
    "What nursery rhyme is never told in Agrabah? Rain Rain Go Away.",
    "Which Princess of Heart is the best at making jokes? Ra-PUN-zel!",
    "What do Xemnas and his army of Nobodies eat right before a race? NOTHING! They fast.",
    "How does Saïx keep his hair so neat? Eclipse it!",
    "What is Pooh’s favorite restaurant? Little Chef’s BEE-stro!",
    "Why can’t Sora go into the library of Beast’s Castle? Cuz it’s already fully booked!",
    "What do you call a search ghost that is having a meltdown at a roller rink? An emotional roller ghoster!",
    "Why does Lexaeus hate working for the Organization? They always take him for granite!",
    "Why is Saïx so obsessed with the moon? Isa don’t know! Why don’t you ask him?",
    "Why didn’t Sora want to play the Cherry Flan minigame? Cuz it was a little off-pudding!",
    "What is Xemnas’s favorite Valentine’s Day hobby? Hearts and Crafts!",
    "What is Sora’s least favorite type of chip? Computer chips!",
    "What song does the Organization sing to Vexen on his birthday? Freeze a jolly good fellow!",
    "Why is Halloweentown Donald so bad at telling lies? Cuz you can see right through him!",
    "Why did Roxas and Jack Skellington go to the ball together? Cuz they both had noBODY else to go with!",
    "Jafar loves Thanksgiving. What’s his favorite holiday phrase? GOBBLE GOBBLE GOBBLE GA!"
    "Why did Sora refuse to play Dark Souls? He said he already died enough emotionally.",
    "What does Demyx call a failed concert? Kingdom Farts.",
    "Why did Goofy install antivirus? He got too many Heartless in his system.",
    "Why can’t Xehanort play rhythm games? He’s always off-beat — and off his meds.",
    "How many Keyblades does it take to fix a lightbulb? None. Riku just broods in the dark.",
    "Why did Aqua stop streaming? She kept falling into the Realm of Lag.",
    "What’s Donald’s favorite loot rarity? Quack-tier.",
    "Why did Roxas quit League of Legends? Too many toxic Nobodies.",
    "How does Axel win at Guitar Hero? He just burns through the competition.",
    "Why did Sora fail his driving test? He kept summoning the Gummi Ship mid-turn.",
    "Why did Goofy try to play FPS games? He wanted to master ‘Goof-shooters’.",
    "Why did the Organization XIII band break up? Too many conflicting hearts.",
    "What’s Xemnas’s favorite social media? None — he has no followers.",
    "Why did Demyx get banned from Twitch? Excessive idle time.",
    "Why doesn’t Kairi play horror games? She’s had enough jump scares named Sora.",
    "Why did Cloud start a podcast? To finally talk about his issues — all seven discs of them.",
    "Why can’t Riku play hide and seek? His aura screams ‘edge detected’.",
    "What’s a Nobody’s least favorite video format? .soul",
    "Why did Namine uninstall Photoshop? Too many layers of trauma.",
    "Why did Sora hate rhythm minigames? He couldn’t ‘Key’ up.",
    "How does Demyx warm up before a show? With Aqua tuning.",
    "What’s the best part about Atlantica? Nothing — it’s a low-tier rhythm hell.",
    "Why did Xion become an artist? Because life drew her that way.",
    "Why did Mickey quit MMO raids? Because Goofy kept pulling aggro IRL.",
    "What’s the most cursed crossover? Kingdom Hearts x Tax Simulator.",
    "Why is Riku banned from Minecraft servers? Too much darkness, not enough torches.",
    "Why did Demyx drop his album on Spotify? Because SoundCloud wouldn’t take water tracks.",
    "Why does Kairi fail every stealth mission? Her heart’s too loud.",
    "Why did Xehanort delete his browser history? To remove his search for ‘how to possess friends ethically’.",
    "What does Sora name every file? FinalMix_FINAL_REAL_THISONE.zip",
    "Why did Aqua start a therapy podcast? Because she’s trapped in everyone’s trauma arc.",
    "How does Axel cool off? He doesn't.",
    "Why does Xemnas hate memes? He can’t feel joy.",
    "Why did Sora cry at the Final Fantasy VII remake? Cloud still doesn’t remember him.",
    "Why is Goofy the best healer? He doesn’t need MP — just vibes.",
    "What’s the scariest thing in Kingdom Hearts? Atlantica’s camera controls.",
    "Why did Roxas stop playing rhythm games? He lost his groove — and his body.",
    "Why did Axel get fired from the pizzeria? Too much fire, not enough dough.",
    "Why did Xehanort start streaming? To collect subscribers — and hearts.",
    "What’s Sora’s favorite snack? Sea-Salt Chips.",
    "Why can’t Larxene play Overwatch? She keeps shocking the payload.",
    "Why did Donald go to therapy? To work on his quack response.",
    "Why does Riku play horror games on mute? He’s already haunted enough.",
    "Why is Aqua’s YouTube channel demonetized? Too much drowning content.",
    "Why did Sora fail Guitar Hero? Because his heart wasn’t in tune.",
    "Why did Demyx refuse to play Fortnite? Too much building — not enough chilling.",
    "Why did the Heartless win karaoke night? They had no soul but killer vocals.",
    "Why did Goofy win best rhythm gamer? Because he’s got perfect ‘goof-timing’.",
    "Why did Xigbar rage quit VRChat? Too much perspective."
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
    "You’ve got less coordination than Sora in Atlantica.",
    "You’re like a failed Keyblade wielder — chosen by mistake and still disappointing.",
    "You play games like Donald heals — never when needed.",
    "You’ve got more lag than Atlantica’s camera controls.",
    "Even a Heartless has more emotional depth than you.",
    "You talk like you skipped the tutorial but still failed the basics.",
    "You’d get benched in Organization XIII for being too useless — and that’s saying something.",
    "If dumb were an element, you’d be the 14th member.",
    "You’d lose a staring contest to Roxas’s blank expression.",
    "You’re like a bad summon — loud, flashy, and totally pointless.",
    "You’ve got less direction than a Gummi Ship built by Goofy.",
    "If being cringe were an ability, you’d be at max level.",
    "You make Atlantica look like a speedrun segment.",
    "Even the shadows think you’re underdeveloped.",
    "You’re the human equivalent of ‘Connection Lost’.",
    "You’ve got less rhythm than Sora mashing X.",
    "You’d get outsmarted by a tutorial Heartless.",
    "You’ve got the personality of a loading screen tip.",
    "You could trip over your own save file.",
    "You’ve got ‘NPC energy’ and it’s not even rare.",
    "You’d fail a QTE labeled ‘Don’t mess this up’.",
    "Even Axel’s hair has more consistency than your life.",
    "You’re like a bug report that never got fixed.",
    "You’ve got less development than KH’s plot timeline.",
    "You remind me of a lag spike — unexpected and unwanted.",
    "You make Atlantica’s singing look like peak gaming.",
    "You’re what happens when RNG gives up.",
    "You’re the side quest no one tracks.",
    "You’d forget your own respawn point.",
    "You’ve got the drip of a default Kingdom Hearts outfit.",
    "Even Demyx’s sitar sounds better than your excuses.",
    "You’ve got less presence than a Nobody in stealth mode.",
    "You’d lose a duel against your own reflection.",
    "You’re like a Keyblade with no keychain — all flash, no function.",
    "You’ve got the vibe of a corrupted save file.",
    "You’d probably miss an attack in turn-based combat.",
    "You talk like you’re buffering mid-sentence.",
    "You’re what happens when someone skips character customization.",
    "You’ve got less flavor than Kingdom Hearts lore in English.",
    "You’re basically Atlantica DLC — nobody asked for you.",
    "You could be replaced by a silent protagonist and nobody would notice.",
    "Even Xaldin’s wind listens better than you do.",
    "You’ve got the same energy as a softlocked game.",
    "You’d lose a boss fight against the pause menu.",
    "You make Goofy look like a critical thinker.",
    "You’re a tutorial that never ends.",
    "You’re the Kingdom Hearts timeline of humans — overly complicated and missing logic.",
    "Even a Drive Form has more color than your personality.",
    "You’re not even a good background NPC — you’re a loading prop.",
    "You’ve got the comedic timing of an unskippable cutscene."\
    "You’ve got more darkness than Xehanort’s search history.",
    "You’d still lose a fight even if you had seven hearts and plot armor.",
    "You’re like a failed replica — cheap, broken, and existentially confused.",
    "If brains were drive forms, you’d still be in base Sora mode.",
    "You’ve got less direction than a Gummi Ship built by Nomura himself.",
    "You look like you got rejected from the Organization for being too depressing.",
    "You’re the kind of person Xemnas points to when he says, ‘See? No hearts.’",
    "Even Saïx at full moon wouldn’t rage that hard at how useless you are.",
    "You’d forget your own name faster than Roxas on a Monday.",
    "You’ve got all of Larxene’s energy but none of her shock value.",
    "You’d trip on your Keyblade trying to look cool.",
    "Even Vexen’s clones have more originality than you.",
    "You make Atlantica look like a good design decision.",
    "You’ve got more bugs than Data Sora’s entire existence.",
    "You’re like Kingdom Hearts’ lore — overcomplicated and still meaningless.",
    "You’ve got the charisma of a Dusk trying to dance.",
    "You’d make Xaldin’s wind attacks look organized.",
    "You’ve got less consistency than Riku’s moral compass.",
    "You’re the unskippable cutscene of human interaction.",
    "You’d still lose to Sephiroth even on beginner mode.",
    "You’ve got more empty space than a Nobody’s heart.",
    "You make Demyx look motivated — and that’s saying something.",
    "You’ve got the vibe of a bad fanfic OC who never got edited.",
    "You’re like a side quest in Traverse Town — pointless and out of the way.",
    "Even the Heartless ignore you out of pity.",
    "You’ve got the emotional depth of a potion tutorial.",
    "You’d fail a friendship test with Donald and Goofy.",
    "You make Xion’s existence look stable.",
    "You’re the reason Yen Sid drinks.",
    "You’d get fired from the Organization for showing initiative — by accident.",
    "You’ve got less rhythm than Atlantica on hard mode.",
    "Even Aqua couldn’t save you from your own mediocrity.",
    "You’re the kind of guy who loses to the tutorial boss and calls it ‘lore’.",
    "You’ve got less plot relevance than Goofy’s shield.",
    "You’re like a corrupted save — tragic and totally your fault.",
    "Even Nomura couldn’t retcon your personality into something interesting.",
    "You’ve got the fighting spirit of a moogle with stage fright.",
    "You’d probably call Xehanort ‘based’ and mean it.",
    "You’re like Sora’s AI partner — jumping in at the worst time possible.",
    "You make Atlantica’s song levels sound like masterpieces.",
    "You’ve got less balance than a Drive Form in tight corridors.",
    "Even the Final Mix couldn’t fix your character.",
    "You’ve got the self-awareness of a Heartless in a light show.",
    "You’re the human equivalent of the ‘Retry’ screen.",
    "You’d die in the prologue and still think you’re the main character.",
    "You’ve got the same energy as a respawn in the Realm of Darkness.",
    "You’re like a summon that crashes the game every time it loads.",
    "You’ve got less precision than Donald’s healing AI.",
    "Even the Kingdom Key deserves a better wielder than you.",
    "You’re a filler boss with main character delusions."
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
    if now.hour == 14 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)

        # 75% chance: fetch from the JokeAPI
        if random.random() < 0.75:
            joke = fetch_joke()
        else:
            joke = random.choice(KH_MUSIC_JOKES)

        emote = random.choice(JOKE_EMOTES)
        if channel:
            await channel.send(f"😂 **Joke of the Day** 😂\n{joke}\n{emote}")

@tree.command(name="joke", description="Demyx tells a random joke from the web 🎭")
async def joke(interaction: discord.Interaction):
    """Fetches a random general joke from JokeAPI (not KH-related)."""
    joke_text = fetch_joke()
    emote = random.choice(JOKE_EMOTES)
    await interaction.response.send_message(f"😂 **Random Joke** 😂\n{joke_text}\n{emote}")


@tree.command(name="khjoke", description="Demyx tells a Kingdom Hearts–inspired joke 💙🗝️")
async def khjoke(interaction: discord.Interaction):
    """Pulls a random Kingdom Hearts joke from the list."""
    joke_text = random.choice(KH_MUSIC_JOKES)
    emote = random.choice(JOKE_EMOTES)
    await interaction.response.send_message(f"🎸 **Kingdom Hearts Joke** 🎸\n{joke_text}\n{emote}")

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
    """Deletes a specified number of recent messages — admin/mod only."""
    try:
        # Acknowledge immediately
        await interaction.response.defer(thinking=True, ephemeral=True)

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.followup.send(
                "🎸 *Demyx strums lazily.* 'Whoa there, rockstar. Only the band leaders get to fade the crowd out.'"
            )
            return

        deleted = await interaction.channel.purge(limit=amount + 1)
        await interaction.followup.send(
            f"🎶 *Demyx grins.* 'And just like that... {len(deleted)-1} messages fade into silence.'"
        )

    except discord.Forbidden:
        await interaction.followup.send(
            "⚠️ *Demyx sighs.* 'Looks like I don’t have permission to delete those, man!'"
        )
    except Exception as e:
        await interaction.followup.send(
            f"⚠️ *Demyx winces.* 'Something went flat — I couldn’t fade those out.'\n`{e}`"
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
    embed.add_field(name="🗝️ /khjoke", value="Tells a Kingdom Hearts–themed joke!", inline=False)
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







