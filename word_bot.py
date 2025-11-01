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
import random

# Riddle
RIDDLES = [
    ("What has keys but can’t open locks?", "A keyboard.", "It makes music or letters."),
    ("I speak without a mouth and hear without ears. What am I?", "An echo.", "You’ll find me in mountains or empty halls."),
    ("The more you take, the more you leave behind. What am I?", "Footsteps.", "Each one marks your path."),
    ("What has to be broken before you can use it?", "An egg.", "Breakfast begins with me."),
    ("What gets wetter the more it dries?", "A towel.", "It helps after a bath."),
    ("What has one eye but can’t see?", "A needle.", "It’s sharp and used for stitching."),
    ("What goes up but never comes down?", "Your age.", "It increases with every birthday."),
    ("What is full of holes but still holds water?", "A sponge.", "You’ll find me by the sink."),
    ("What has many teeth but cannot bite?", "A comb.", "It smooths but never eats."),
    ("What can travel around the world while staying in the corner?", "A stamp.", "It clings to letters and journeys far."),
    ("The more of this there is, the less you see. What is it?", "Darkness.", "Light’s eternal opposite."),
    ("I’m tall when I’m young, and short when I’m old. What am I?", "A candle.", "I melt as I work."),
    ("What has hands but can’t clap?", "A clock.", "It marks time but never rests."),
    ("What has a head, a tail, but no body?", "A coin.", "I’m used in decisions of chance."),
    ("What runs but never walks?", "Water.", "You drink me every day."),
    ("What kind of room has no doors or windows?", "A mushroom.", "It grows in damp, dark places."),
    ("What gets sharper the more you use it?", "Your mind.", "Knowledge is my whetstone."),
    ("What can you catch but not throw?", "A cold.", "It comes with sneezes and rest."),
    ("What word becomes shorter when you add two letters to it?", "Short.", "It’s self-referential."),
    ("What begins with T, ends with T, and has T in it?", "A teapot.", "A drink’s favorite home."),
    ("What can fill a room but takes up no space?", "Light.", "I chase away the dark."),
    ("What has a neck but no head?", "A bottle.", "I often hold something to drink."),
    ("The more you take away, the bigger I get. What am I?", "A hole.", "You’ll find me in the ground."),
    ("What invention lets you look right through a wall?", "A window.", "Clear but not invisible."),
    ("What has an eye but cannot see and is formed in the sky?", "A hurricane.", "Born from storms."),
    ("What flies without wings?", "Time.", "It’s always moving forward."),
    ("What’s always in front of you but can’t be seen?", "The future.", "You walk toward it every second."),
    ("What can run but never walks, has a bed but never sleeps?", "A river.", "Follow my current."),
    ("What’s black when it’s clean and white when it’s dirty?", "A chalkboard.", "Teachers use me daily."),
    ("What begins with an E but only has one letter?", "An envelope.", "Mail’s paper vessel."),
    ("What belongs to you but others use it more than you?", "Your name.", "It identifies you in sound."),
    ("What’s easy to lift but hard to throw?", "A feather.", "A bird carries me effortlessly."),
    ("What’s always moving but never gets tired?", "A clock.", "Tick by tick, I go on."),
    ("What can’t talk but replies when spoken to?", "An echo.", "You’ll find me in canyons or caves."),
    ("What can fly without wings and cry without eyes?", "A cloud.", "I float and weep from the sky."),
    ("What gets broken without being held?", "A promise.", "Words can shatter me."),
    ("What kind of band never plays music?", "A rubber band.", "I’m stretchy and silent."),
    ("What’s so fragile that saying its name breaks it?", "Silence.", "I exist only until sound arrives."),
    ("What has roots that nobody sees and is taller than trees?", "A mountain.", "My peak touches the clouds."),
    ("What comes once in a minute, twice in a moment, but never in a thousand years?", "The letter M.", "You’ll find me in words, not time."),
    ("What has four fingers and a thumb but isn’t alive?", "A glove.", "It warms your hands."),
    ("What can you hold in your left hand but not in your right?", "Your right elbow.", "A twist of perspective."),
    ("What can’t be seen but is always coming?", "Tomorrow.", "You can’t stop my arrival."),
    ("What can you break, even if you never pick it up?", "A promise.", "Trust depends on me."),
    ("What has cities but no houses, forests but no trees, and rivers but no water?", "A map.", "I show the world but hold none of it."),
    ("What can one not keep until it is given?", "A promise.", "Shared words bind it."),
    ("What disappears as soon as you say its name?", "Silence.", "Speech destroys me."),
    ("What has legs but doesn’t walk?", "A table.", "Dinner is served on me."),
    ("What’s mine but only used by others?", "Your name.", "Others speak it for you."),
    ("What’s lighter than a feather but the strongest man can’t hold it for long?", "Your breath.", "You need me to live."),
    ("What’s the beginning of eternity, the end of time, and the beginning of every end?", "The letter E.", "I’m a letter, not a concept.")
]

# Quote about words or KH-style wisdom
QUOTES = [
    "🕯️ 'Knowledge lights the path where hearts have lost their way.'",
    "📜 'Words are the echoes of memory.'",
    "🔮 'Light and darkness are both teachers — it depends on who listens.'",
    "🌌 'Even silence speaks, if one knows how to read it.'",
    "📚 'A heart that seeks knowledge never truly fades into darkness.'",
    "📖 'Every word is a fragment of truth, waiting for a mind to complete it.'",
    "🕯️ 'In the silence between pages, understanding is born.'",
    "🌒 'Darkness is not ignorance — only the absence of discovery.'",
    "📚 'To read is to listen to voices long since faded.'",
    "🌌 'Light reveals form, but darkness reveals depth.'",
    "🔮 'A heart without curiosity is a book never opened.'",
    "📜 'Knowledge is the one thing that grows when shared.'",
    "🌗 'Even shadows have meaning when cast by the right light.'",
    "🪶 'The pen remembers what the heart cannot.'",
    "🕯️ 'Every truth begins as a whisper in the dark.'",
    "📘 'Words shape hearts more deeply than any Keyblade.'",
    "🌙 'The wise do not flee from darkness — they study it.'",
    "🌀 'Understanding and doubt walk hand in hand through the corridors of thought.'",
    "📚 'To seek knowledge is to chase the horizon — always seen, never reached.'",
    "💫 'Every heart holds a library of its own — some just forget how to read it.'",
    "🔮 'Illusions fade, but the lessons they teach remain.'",
    "🕯️ 'Light teaches by warmth, darkness by reflection.'",
    "📖 'The mind is a labyrinth; words are its map.'",
    "🌌 'When hearts connect, knowledge flows freely — like stars joining constellations.'",
    "📜 'Even in silence, the lexicon speaks to those who listen.'"
    
]
# === Organization XIII Archives ===
ORGANIZATION_QUOTES = [
    # Xemnas
    "📖 *Zexion adjusts his lexicon.* 'I can’t help but recall Xemnas once proclaiming, “Emptiness isn’t a void to be feared — it’s a canvas waiting for meaning.”'",
    "📖 *Zexion muses softly.* 'There was a time when Xemnas declared, “Power is never enough when the heart remains unanswered.”'",
    "📖 *Zexion lowers his gaze.* 'I still remember Xemnas musing, “To lead nothingness, one must first accept that they, too, are nothing.”'",

    # Xigbar (Braig)
    "🎯 *Zexion sighs faintly.* 'I’m reminded of how Xigbar laughed, “Everyone’s aiming for the top, but the real fun’s in knocking them off it.”'",
    "🎯 *Zexion smirks slightly.* 'It takes me back to when Xigbar teased, “Perspective changes everything — especially when you’re hanging upside down.”'",
    "🎯 *Zexion tilts his head.* 'Sometimes I can hear Xigbar smirking, “I don’t need a heart to enjoy watching the game unfold.”'",

    # Xaldin
    "🌪️ *Zexion recalls solemnly.* 'It echoes in my mind how Xaldin once growled, “Love is the storm that makes men weak.”'",
    "🌪️ *Zexion nods thoughtfully.* 'I think of the time Xaldin stated, “Control is not about strength — it’s about taming the wind that refuses to bow.”'",
    "🌪️ *Zexion closes his eyes briefly.* 'There was a grim moment when Xaldin muttered, “Emotions are tempests best left to those who drown in them.”'",

    # Vexen (Even)
    "❄️ *Zexion adjusts his tone.* 'I recall Vexen lecturing once, “Science thrives where emotion decays.”'",
    "❄️ *Zexion’s expression sharpens.* 'It’s hard to forget when Vexen scoffed, “Perfection is only achieved when all variables are under your thumb.”'",
    "❄️ *Zexion adds quietly.* 'I can still picture Vexen noting coldly, “The heart is a reckless organ; the mind is its reluctant keeper.”'",

    # Lexaeus (Aeleus)
    "🪨 *Zexion speaks with quiet respect.* 'There was a rare moment of calm when Lexaeus rumbled, “Strength is silent — it doesn’t need to announce itself.”'",
    "🪨 *Zexion continues.* 'I once heard Lexaeus say, “Even the earth listens when you move with purpose.”'",
    "🪨 *Zexion reflects.* 'I often recall Lexaeus remarking, “Discipline weighs less than regret.”'",

    # Saïx (Isa)
    "🌕 *Zexion murmurs softly.* 'Every so often, I recall Saïx uttering, “The moon watches, but never interferes — I envy that.”'",
    "🌕 *Zexion frowns slightly.* 'I think back to Saïx growling, “Order is the only thing that keeps the beast inside from breaking free.”'",
    "🌕 *Zexion lowers his tone.* 'It’s almost haunting when I remember Saïx muttering, “Control isn’t calm — it’s chaos buried under will.”'",

    # Axel (Lea)
    "🔥 *Zexion half-smiles.* 'It’s funny — I still remember Axel grinning, “Flames don’t apologize for burning — they just light the way.”'",
    "🔥 *Zexion chuckles quietly.* 'Once, Axel joked, “If you can’t stand the heat, you’re probably doing it right.”'",
    "🔥 *Zexion’s voice softens.* 'And I’ll never forget Axel saying, “Friendship isn’t about hearts — it’s about who’s still there when things burn down.”'",

    # Demyx
    "🎸 *Zexion shakes his head with faint amusement.* 'It always cracks me up thinking of Demyx laughing, “Why fight the current when you can just float with the melody?”'",
    "🎸 *Zexion sighs in thought.* 'I remember Demyx saying once, “Not everyone’s built to be a hero — some of us are just the soundtrack.”'",
    "🎸 *Zexion smirks.* 'Can’t forget how Demyx shrugged, “If laziness were a sin, I’d still be too lazy to care.”'",

    # Luxord
    "♠️ *Zexion taps his chin.* 'Every now and then, I think of Luxord musing, “Every hand you play is a wager with fate — some just bluff better.”'",
    "♣️ *Zexion muses softly.* 'There was a time when Luxord remarked, “Time folds neatly for those who know how to bet against it.”'",
    "♦️ *Zexion smiles faintly.* 'I can still hear Luxord chuckling, “The house always wins — unless you make the rules.”'",

    # Marluxia
    "🌸 *Zexion turns a page delicately.* 'I still recall Marluxia whispering, “Beauty blooms best when it’s dangerous.”'",
    "🌺 *Zexion sighs faintly.* 'It’s impossible to forget when Marluxia declared, “Petals fall — but the thorns always remain.”'",
    "🌹 *Zexion muses.* 'I once heard Marluxia purr, “Power, like a rose, needs pruning to keep its elegance.”'",

    # Larxene
    "⚡ *Zexion frowns slightly.* 'I’ll never forget how Larxene laughed, “Pain’s just another spark — the fun part is watching it spread.”'",
    "⚡ *Zexion shakes his head.* 'I think of Larxene teasing, “I don’t do nice — I do honest, and it stings.”'",
    "⚡ *Zexion adds coolly.* 'Still hear Larxene hissing, “Lightning doesn’t ask for permission to strike.”'",

    # Roxas
    "☀️ *Zexion looks distant.* 'I often remember Roxas saying, “If I don’t know who I am, maybe I can still choose who I want to be.”'",
    "☀️ *Zexion’s voice softens.* 'I can still picture Roxas admitting, “Having no heart doesn’t mean I can’t feel the emptiness.”'",
    "☀️ *Zexion turns a page slowly.* 'And there’s that quiet moment where Roxas murmured, “Sometimes the hardest thing is realizing you were never supposed to exist — but doing it anyway.”'",

    # Xion
    "🌙 *Zexion speaks gently.* 'Sometimes I think back to Xion whispering, “Even borrowed memories can feel like home.”'",
    "🌙 *Zexion closes his book momentarily.* 'I’ll always remember Xion saying softly, “I’m not real — but that doesn’t mean I’m nothing.”'",
    "🌙 *Zexion looks thoughtful.* 'And I still hear Xion confessing, “If forgetting me brings you peace, then I’ll fade with a smile.”'"
]

# === Additional Organization XIII Archives ===


ORGANIZATION_QUOTES += [
    "📖 *Zexion reflects quietly.* 'Xemnas once told me, “To exist without purpose is the cruelest fate.”'",
    "📖 *Zexion muses.* 'I remember Xemnas saying, “Hearts are fragile things — that’s why we replaced them with resolve.”'",
    "📖 *Zexion turns a page slowly.* 'Xemnas often reminded us, “Even a void has order — we merely gave it a name.”'",
    "📖 *Zexion murmurs.* 'There was a time Xemnas said, “Emotion is a luxury for those who still believe they exist.”'",
    "📖 *Zexion adds softly.* 'I once heard Xemnas claim, “We are echoes — but even echoes can change the tone of eternity.”'",

    # Xigbar (Braig)
    "🎯 *Zexion smirks faintly.* 'Xigbar once chuckled, “You can’t fall if you never stop aiming sideways.”'",
    "🎯 *Zexion shrugs slightly.* 'I recall him saying, “Half of surviving is pretending you’re not surprised.”'",
    "🎯 *Zexion sighs.* 'He used to laugh, “A straight shot’s boring — ricochets make life interesting.”'",
    "🎯 *Zexion muses.* 'Once, Xigbar said, “Loyalty’s just a fancy way of saying ‘I’m not done yet.’”'",
    "🎯 *Zexion smiles faintly.* 'I remember him grinning, “The view’s best when you’re above it all — literally.”'",

    # Xaldin
    "🌪️ *Zexion notes quietly.* 'Xaldin once said, “The wind is honest — it cuts without malice.”'",
    "🌪️ *Zexion reflects.* 'He used to mutter, “Love is weakness disguised as poetry.”'",
    "🌪️ *Zexion muses.* 'I remember Xaldin saying, “Power demands restraint — otherwise it devours the one who wields it.”'",
    "🌪️ *Zexion sighs.* 'He once remarked, “The calm before the storm is just the storm waiting to be born.”'",
    "🌪️ *Zexion lowers his voice.* 'Xaldin once told me, “Even the wind obeys strength it respects.”'",

    # Vexen (Even)
    "❄️ *Zexion smiles thinly.* 'Vexen once declared, “Ignorance is contagious — but knowledge is terminal.”'",
    "❄️ *Zexion recalls.* 'He said, “The experiment is never the failure — only the subject.”'",
    "❄️ *Zexion muses.* 'I remember Vexen warning, “Emotion corrupts data faster than decay.”'",
    "❄️ *Zexion tilts his head.* 'He once told me, “Truth is an equation — emotion is its flaw.”'",
    "❄️ *Zexion’s tone chills.* 'I recall him whispering, “A frozen heart is the most stable compound of all.”'",

    # Lexaeus (Aeleus)
    "🪨 *Zexion nods respectfully.* 'Lexaeus once said, “Patience is the weight that keeps wisdom grounded.”'",
    "🪨 *Zexion recalls softly.* 'He told me, “A strong hand can lift others — or crush them. Choose wisely.”'",
    "🪨 *Zexion muses.* 'I remember Lexaeus saying, “Stone remembers every step taken upon it.”'",
    "🪨 *Zexion continues.* 'He once rumbled, “True strength is measured in restraint, not force.”'",
    "🪨 *Zexion reflects.* 'I recall him saying, “Quiet minds move mountains.”'",

    # Saïx (Isa)
    "🌕 *Zexion speaks lowly.* 'Saïx once murmured, “The moon’s pull is cruel — it moves the tides, but never the sea.”'",
    "🌕 *Zexion frowns.* 'He once told me, “Loyalty without purpose is just another chain.”'",
    "🌕 *Zexion muses.* 'I recall him saying, “Pain is order’s reminder that chaos still breathes.”'",
    "🌕 *Zexion continues.* 'He used to whisper, “The stars are patient — they burn quietly while we rage.”'",
    "🌕 *Zexion sighs faintly.* 'Saïx once said, “Even the moon hides its scars behind the light.”'",

    # Axel (Lea)
    "🔥 *Zexion chuckles softly.* 'Axel once grinned, “A flame doesn’t ask why — it just burns until it can’t.”'",
    "🔥 *Zexion smiles faintly.* 'I remember Axel saying, “If you can’t handle the burn, you never deserved the spark.”'",
    "🔥 *Zexion muses.* 'He used to say, “Every light leaves a shadow — that’s where I feel most alive.”'",
    "🔥 *Zexion continues.* 'Once, Axel smirked, “Friendship’s just flammable trust.”'",
    "🔥 *Zexion adds quietly.* 'I recall him murmuring, “When the ashes settle, who’s still standing matters most.”'",

    # Demyx
    "🎸 *Zexion sighs lightly.* 'Demyx once said, “Silence is just music waiting to be played.”'",
    "🎸 *Zexion chuckles.* 'He used to grin, “Responsibility’s a bad rhythm — I prefer improvisation.”'",
    "🎸 *Zexion smirks.* 'I remember him saying, “Water doesn’t fight the shape — it becomes it.”'",
    "🎸 *Zexion muses.* 'Demyx once said, “If you play long enough, even chaos finds a tempo.”'",
    "🎸 *Zexion laughs softly.* 'He once admitted, “I practice apathy — it’s the only art I’ve mastered.”'",

    # Luxord
    "♠️ *Zexion smirks faintly.* 'Luxord once told me, “Luck isn’t chance — it’s timing disguised.”'",
    "♣️ *Zexion muses softly.* 'He used to say, “Every decision is a card already dealt — you just don’t see it yet.”'",
    "♦️ *Zexion tilts his head.* 'I recall him saying, “Patience is the gambler’s greatest bluff.”'",
    "♠️ *Zexion nods thoughtfully.* 'He once remarked, “Fate’s a dealer with endless decks — play smart, not long.”'",
    "♣️ *Zexion smiles faintly.* 'I remember Luxord saying, “If time’s the game, I’ve already won by wasting yours.”'",

    # Marluxia
    "🌸 *Zexion muses softly.* 'Marluxia once said, “Decay is beauty’s cruelest admirer.”'",
    "🌺 *Zexion sighs lightly.* 'He used to remark, “Control is just another word for elegance.”'",
    "🌹 *Zexion continues.* 'I recall him whispering, “Thorns remind the world that beauty has defenses.”'",
    "🌸 *Zexion smiles faintly.* 'He once told me, “Death is the only soil that true growth needs.”'",
    "🌹 *Zexion adds quietly.* 'Marluxia once purred, “A single bloom can outlast an empire if it refuses to wilt.”'",

    # Larxene
    "⚡ *Zexion grimaces slightly.* 'Larxene once hissed, “A spark’s worth more than a thousand kind words.”'",
    "⚡ *Zexion sighs.* 'She used to laugh, “Kindness is boring — pain makes better conversation.”'",
    "⚡ *Zexion muses.* 'I recall her smirking, “If they don’t flinch, you’re not doing it right.”'",
    "⚡ *Zexion shakes his head.* 'She once said, “Lightning teaches fast learners — or kills the slow.”'",
    "⚡ *Zexion adds softly.* 'Larxene once told me, “If you want honesty, ask someone cruel.”'",

    # Roxas
    "☀️ *Zexion speaks gently.* 'Roxas once said, “Even a Nobody can make a choice that matters.”'",
    "☀️ *Zexion recalls softly.* 'He told me, “If I fade, I hope someone remembers I tried.”'",
    "☀️ *Zexion muses.* 'I remember Roxas whispering, “Light doesn’t ask — it simply shines.”'",
    "☀️ *Zexion continues.* 'He once said, “A borrowed heart still beats if you listen closely.”'",
    "☀️ *Zexion smiles faintly.* 'Roxas told me, “Maybe I was never supposed to exist — but I’ll live like I did.”'",

    # Xion
    "🌙 *Zexion reflects softly.* 'Xion once said, “Even false memories can carry real feelings.”'",
    "🌙 *Zexion adds quietly.* 'She used to whisper, “If I am a copy, then let me be an original failure.”'",
    "🌙 *Zexion muses.* 'I recall her saying, “Names fade — but kindness lingers longer than truth.”'",
    "🌙 *Zexion sighs softly.* 'She once told me, “If I disappear, let the wind remember my song.”'",
    "🌙 *Zexion closes his lexicon slowly.* 'Xion once said, “Existing for a moment is still more than never being at all.”'"
]


# === Zexion's Intros ===

# Light Intros (for daytime)
LIGHT_INTROS = [
    "📖 *Zexion opens an ancient lexicon...* 'Ah, here’s a word worth knowing today.'",
    "🕯️ *In the quiet halls of Ansem the Wise’s castle, Zexion whispers:* 'Today’s word shall enrich your mind.'",
    "📚 'Gather close, wielders of light,' Zexion says with a knowing smile. 'Let us learn a new word.'",
    "🌞 'Knowledge is the dawn that follows darkness,' Zexion says softly. 'Let it guide you today.'",
    "📜 *Sunlight spills across old pages as Zexion turns them.* 'Words shine brightest when shared.'",
    "🪶 'The light of understanding is a gift we pass along,' Zexion muses, closing his lexicon with care.",
    "🌤️ 'Even the smallest word can brighten the heart,' Zexion remarks as he begins today’s lesson.",
    "💫 *Zexion smiles faintly.* 'The pursuit of light begins with a single word.'"
]

# Dark Intros (for nighttime)
DARK_INTROS = [
    "🌒 *Zexion turns a page within the shadows.* 'Even in darkness, knowledge is a beacon.'",
    "🔮 'Words are the threads of reality itself,' Zexion murmurs. 'Today, we weave a new one.'",
    "🌌 *Gazing into the abyss between worlds, Zexion muses:* 'Each word holds a fragment of the heart.'",
    "🕯️ *From the Realm of Darkness, Zexion’s voice echoes softly:* 'Even lost hearts remember the language of light.'",
    "🌑 'The night conceals truth, yet words illuminate what eyes cannot,' Zexion murmurs.",
    "🕯️ *Within the corridors of memory, Zexion whispers:* 'Even forgotten words have power.'",
    "🌘 'Darkness is not absence... only a deeper lesson,' Zexion says, eyes glinting with thought.",
    "🕯️ *Pages rustle in the dim glow.* 'Another word to bind the shadows and the light.'"
]
# Insight
INSIGHTS = [
    "🔮 'The heart may forget, but words remember.'",
    "🌒 'Only in silence can truth be heard.'",
    "📚 'To understand the light, one must first read the dark.'"
]
# Track active riddles by user
ACTIVE_RIDDLES = {}

# === Helper: Choose intro based on UTC time ===
def get_zexion_intro():
    """Pick a Light or Dark intro depending on the time of day."""
    now_utc = datetime.utcnow()
    hour = now_utc.hour

    # Convert time: 11 AM–11 PM UTC = 6 AM–6 PM EST (Light)
    if 11 <= hour < 23:
        theme = "LIGHT"
        intro = random.choice(LIGHT_INTROS)
    else:
        theme = "DARK"
        intro = random.choice(DARK_INTROS)

    print(f"🕒 Theme selected: {theme} (UTC hour {hour})")
    return intro

  
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
    await tree.sync()
    print("🌐 Slash commands synced.")
    post_word_of_day.start()  # ✅ must be inside the function, not indented weirdly

# --- Scheduled WOTD (9:00 AM) ---
@tasks.loop(minutes=1)
async def post_word_of_day():
    """Post Word of the Day at 9:00 AM EST (14:00 UTC)."""
    try:
        now = datetime.utcnow()
        print("⏰ Checking UTC time:", now)
        if now.hour == 14 and now.minute == 0:
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                intro = get_zexion_intro()  # 👈 pick Light/Dark intro
                word, definition = fetch_word_of_the_day()
                message = f"{intro}\n\n📚 **Word of the Day**: **{word}**\n{definition}"
                await channel.send(message)
            else:
                print("⚠️ Could not find channel.")
    except Exception as e:
        print("❌ Error in post_word_of_day:", e)

# --- Slash Commands ---
@tree.command(name="ping", description="Check if the bot is online 🏓")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

@tree.command(name="wotd", description="Get today's Word of the Day 📚")
async def wotd(interaction: discord.Interaction):
    word, definition = fetch_word_of_the_day()
    await interaction.response.send_message(f"📚 **Word of the Day**: **{word}**\n{definition}")
  
@tree.command(name="randomword", description="Zexion reveals a random word with Light or Dark energy.")
async def randomword(interaction: discord.Interaction):
    intro = get_zexion_intro()
    word, definition = fetch_word_of_the_day()
    await interaction.response.send_message(f"{intro}\n\n📚 **Word of the Day**: **{word}**\n{definition}")

@tree.command(name="define", description="Define any word — Zexion consults his lexicon.")
@app_commands.describe(word="The word you want Zexion to define.")
async def define(interaction: discord.Interaction, word: str):
    """Fetches and displays the definition of a word from Wordnik."""
    try:
        # Step 1: Build the Wordnik API URL
        url = f"https://api.wordnik.com/v4/word.json/{word}/definitions"
        params = {"limit": 1, "api_key": WORDNIK_API_KEY}

        # Step 2: Request the definition
        response = requests.get(url, params=params, timeout=10)

        # Step 3: Check if it worked
        if response.status_code == 200:
            data = response.json()
            if data:
                definition = data[0].get("text", "No definition found.")
                cleaned_def = re.sub(r"<.*?>", "", definition)
                await interaction.response.send_message(
                    f"📖 *Zexion flips through his lexicon...*\n**{word.capitalize()}** — {cleaned_def}"
                )
            else:
                await interaction.response.send_message(f"❌ No definition found for **{word}**.")
        else:
            await interaction.response.send_message(f"⚠️ Could not fetch definition for **{word}**.")
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}")


# Synonyms
@tree.command(name="synonyms", description="Zexion weaves together words of similar meaning.")
@app_commands.describe(word="The word you wish to find synonyms for.")
async def synonyms(interaction: discord.Interaction, word: str):
    """Fetches synonyms for a word from Wordnik."""
    try:
        url = f"https://api.wordnik.com/v4/word.json/{word}/relatedWords"
        params = {"relationshipTypes": "synonym", "api_key": WORDNIK_API_KEY}
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data:
                synonyms_list = data[0].get("words", [])
                if synonyms_list:
                    formatted = ", ".join(synonyms_list[:10])
                    await interaction.response.send_message(
                        f"🪶 *Zexion muses...* 'Words that share kinship with **{word}** include:'\n{formatted}"
                    )
                    return
            await interaction.response.send_message(f"❌ No synonyms found for **{word}**.")
        else:
            await interaction.response.send_message(f"⚠️ Could not fetch synonyms for **{word}**.")
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}")


# Antonyms
@tree.command(name="antonyms", description="Zexion reveals words that oppose your query — the balance of meaning.")
@app_commands.describe(word="The word you wish to find antonyms for.")
async def antonyms(interaction: discord.Interaction, word: str):
    """Fetches antonyms for a word from Wordnik."""
    try:
        url = f"https://api.wordnik.com/v4/word.json/{word}/relatedWords"
        params = {"relationshipTypes": "antonym", "api_key": WORDNIK_API_KEY}
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data:
                antonyms_list = data[0].get("words", [])
                if antonyms_list:
                    formatted = ", ".join(antonyms_list[:10])
                    await interaction.response.send_message(
                        f"🌒 *Zexion whispers...* 'In opposition to **{word}**, you’ll find:'\n{formatted}"
                    )
                    return
            await interaction.response.send_message(f"❌ No antonyms found for **{word}**.")
        else:
            await interaction.response.send_message(f"⚠️ Could not fetch antonyms for **{word}**.")
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}")


@tree.command(name="quote", description="Zexion shares a quote about knowledge or wisdom.")
async def quote(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(QUOTES + ORGANIZATION_QUOTES))




# Library / help command
@tree.command(name="library", description="Zexion reveals the contents of his lexicon — all available commands.")
async def library(interaction: discord.Interaction):
    """Lists all available commands with lore-flavored descriptions."""
    message = (
        "📘 *Zexion opens his lexicon, eyes glinting with knowledge...*\n\n"
        "Here’s what I can offer you, **wielder of light and thought**:\n\n"
        "🪶 **/define** — I will reveal the meaning of any word, as written in the pages of knowledge.\n"
        "🔗 **/synonyms** — I’ll weave together words that share the same essence.\n"
        "⚖️ **/antonyms** — I’ll expose the words that oppose — balance through contrast.\n"
        "📜 **/etymology** — I shall trace the history of a word through time itself.\n"
        "🕯️ **/quote** — Hear wisdom from my archives — truths gathered in shadow and light.\n"
        "🌀 **/riddle** — Test your mind against a challenge from my collection.\n"
        "💡 **/hint** — Should you falter, I will grant you a whisper of guidance.\n"
        "📖 **/library** — You’ve already opened this page — the index of my entire lexicon.\n\n"
        "‘Knowledge is not meant to be hoarded — only understood.’"
    )

    await interaction.response.send_message(message)

@tree.command(name="riddle", description="Zexion tests your mind with a riddle.")
async def riddle(interaction: discord.Interaction):
    question, answer = random.choice(RIDDLES)
    ACTIVE_RIDDLES[interaction.user.id] = answer
    await interaction.response.send_message(
        f"🌀 *Zexion smirks.* '{question}'\n\n'Solve this, if your mind is sharp...'"
    )
@tree.command(name="hint", description="Request a cryptic hint from Zexion about your current riddle.")
async def hint(interaction: discord.Interaction):
    # Check if user has a riddle active
    active_riddle = ACTIVE_RIDDLES.get(interaction.user.id)
    if not active_riddle:
        await interaction.response.send_message("🕯️ *Zexion closes his lexicon.* 'You have no riddle to ponder, seeker of knowledge.'")
        return

    # Find the matching riddle in the list
    for q, a, *rest in RIDDLES:
        if a == active_riddle:
            hint_text = rest[0] if rest else "🌀 *Zexion smirks.* 'No hint for this one... you must rely on wit alone.'"
            await interaction.response.send_message(f"🔮 *Zexion sighs and murmurs:* '{hint_text}'")
            return

    await interaction.response.send_message("🌫️ *Zexion frowns.* 'The lexicon offers no clue for this riddle.'")

@tree.command(name="answer", description="Attempt to solve Zexion’s riddle.")
async def answer(interaction: discord.Interaction, guess: str):
    answer = ACTIVE_RIDDLES.get(interaction.user.id)
    if not answer:
        await interaction.response.send_message("🕯️ *Zexion raises a brow.* 'You have no active riddle to solve.'")
        return

    if guess.lower() in answer.lower():
        await interaction.response.send_message(f"💫 *Zexion nods and smiles ever so slightly in your direction, almost as if he is proud, almost.* 'Correct. The answer was indeed {answer}.'")
    else:
        await interaction.response.send_message(f"🌒 *Zexion scowls in disappointment, smacking you with his heavy Lexicon. You should feel ashamed.* 'Not quite. The answer was {answer}.'")

    del ACTIVE_RIDDLES[interaction.user.id]

@tree.command(name="insight", description="Zexion shares a philosophical thought.")
async def insight(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(INSIGHTS))


# Etymology
@tree.command(name="etymology", description="Zexion reveals the origin of a word — tracing its roots through time.")
@app_commands.describe(word="The word you want Zexion to analyze.")
async def etymology(interaction: discord.Interaction, word: str):
    """Fetches, cleans, and presents a word's etymology with poetic flavor."""
    try:
        url = f"https://api.wordnik.com/v4/word.json/{word}/etymologies"
        params = {"api_key": WORDNIK_API_KEY}
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data:
                raw_etymology = data[0]

                # 🧹 Clean raw text
                cleaned = re.sub(r"<.*?>", "", raw_etymology)             # remove HTML tags
                cleaned = re.sub(r"\[.*?\]", "", cleaned)                 # remove [AS. le√≥ht.] or [L. ...]
                cleaned = re.sub(r"See .*?\.", "", cleaned)               # remove "See Light, n." type endings
                cleaned = re.sub(r"√≥", "g", cleaned)                     # fix encoding glitch
                cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()         # clean spacing

                # 🧙‍♂️ If cleaned is too short or unclear, fallback line
                if not cleaned or len(cleaned.split()) < 3:
                    cleaned = "The origin of this word has been obscured by time — even the lexicon whispers uncertainty."

                # 🎭 Zexion’s poetic variants
                intros = [
                    f"📜 *Zexion adjusts his spectacles and flips through his lexicon...* 'Ah, {word.capitalize()}... its origin is quite fascinating.'",
                    f"🔮 *Within the quiet of the archives, Zexion murmurs:* 'Let us trace the roots of **{word.capitalize()}** through the corridors of language.'",
                    f"📖 *Pages flutter as Zexion turns them slowly.* 'Every word carries a memory — and **{word.capitalize()}** is no exception.'",
                    f"🌒 *Zexion’s voice echoes softly in the dark hall.* 'Once, long ago, **{word.capitalize()}** took shape from ancient tongues...'",
                    f"🕯️ *By candlelight, Zexion muses:* 'Even words have ancestry. Observe the path of **{word.capitalize()}**.'"
                ]

                outro_lines = [
                    "Such origins remind us that meaning, like light, changes with time.",
                    "Even the simplest word may carry centuries of transformation.",
                    "Its history mirrors the shifting balance between memory and meaning.",
                    "The lexicon never forgets — it merely waits to be read again.",
                    "Knowledge endures, even when the tongues that spoke it have long since fallen silent."
                ]

                intro = random.choice(intros)
                outro = random.choice(outro_lines)

                # 🕯️ Final message
                message = f"{intro}\n\n**Etymology:** {cleaned}\n\n_{outro}_"
                await interaction.response.send_message(message)
            else:
                await interaction.response.send_message(f"❌ No etymology found for **{word}**.")
        else:
            await interaction.response.send_message(f"⚠️ Could not fetch etymology for **{word}**.")
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}")


# Mood (Light / Dark)
@tree.command(name="mood", description="Zexion reveals whether it is Light or Dark hour.")
async def mood(interaction: discord.Interaction):
    now_utc = datetime.utcnow()
    hour = now_utc.hour
    if 11 <= hour < 23:
        await interaction.response.send_message("☀️ *Zexion adjusts his glasses.* 'The light of day guides us now.'")
    else:
        await interaction.response.send_message("🌒 *Zexion’s voice echoes softly.* 'Darkness settles... tread carefully through thought.'")


# Observe / Remember / Reflect (flavor quotes)
@tree.command(name="observe", description="Zexion shares an observation about words or hearts.")
async def observe(interaction: discord.Interaction):
    lines = [
        "📖 'Every heart writes its own story — some just fade before the final page.'",
        "🔮 'Observation is the first step toward understanding... and the last toward judgment.'"
    ]
    await interaction.response.send_message(random.choice(lines))


@tree.command(name="remember", description="Zexion recalls something from Ansem’s archives.")
async def remember(interaction: discord.Interaction):
    lines = [
        "📜 *Zexion reads from Ansem’s notes:* 'Even a heart devoid of light still seeks meaning.'",
        "🕯️ 'Ansem once wrote: Knowledge is the shadow cast by curiosity.'"
    ]
    await interaction.response.send_message(random.choice(lines))


@tree.command(name="reflect", description="Zexion reflects on the balance between light and dark.")
async def reflect(interaction: discord.Interaction):
    lines = [
        "🌗 'The line between light and dark is not a wall... but a mirror.'",
        "🌑 'To reflect is to see both sides of the same truth.'"
    ]
    await interaction.response.send_message(random.choice(lines))

@tree.command(name="wipe", description="Zexion erases traces of past words — only those of authority may do so.")
@app_commands.describe(amount="How many recent messages to erase (default: 5).")
async def wipe(interaction: discord.Interaction, amount: int = 5):
    """Deletes a number of recent messages — restricted to admins or those with Manage Messages."""
    # Check if user has admin or manage message permissions
    if not interaction.user.guild_permissions.manage_messages and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "🚫 *Zexion closes his lexicon with a sharp snap.* 'Only those entrusted with order may cleanse the archives.'",
            ephemeral=True
        )
        return

    # Ensure it’s used in a text channel
    if not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message(
            "⚠️ *Zexion frowns slightly.* 'This spell functions only within the written halls — text channels, to be precise.'",
            ephemeral=True
        )
        return

    # Perform the purge
    try:
        deleted = await interaction.channel.purge(limit=amount + 1)  # include the command message
        await interaction.response.send_message(
            f"🕯️ *Zexion silently erases {len(deleted) - 1} entries from the archives...*",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ *Zexion grimaces.* 'The lexicon resisted the purge: {e}'",
            ephemeral=True
        )

# === Run Bot ===
bot.run(DISCORD_TOKEN)










