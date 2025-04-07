# Library Import
import discord  
import asyncio
import random

# Discord Library Import
from discord.ext import commands

# Functions File Import
from functions import get_ai_response
from functions import translate_text

# Discord Token

# Global Variables
language_map = { "albanian": "sq", "amharic": "am", "arabic": "ar", "armenian": "hy", "basque": "eu", "bengali": "bn", "bosnian": "bs", "bulgarian": "bg", "catalan": "ca", "chichewa": "ny", "chinese": "zh-CN", "croatian": "hr", "czech": "cs", "danish": "da", "dutch": "nl", "english": "en", "estonian": "et", "farsi": "fa", "filipino": "tl", "finnish": "fi", "french": "fr", "georgian": "ka", "german": "de", "greek": "el", "haitian creole": "ht", "hebrew": "he", "hindi": "hi", "hungarian": "hu", "icelandic": "is", "indonesian": "id", "irish": "ga", "italian": "it", "japanese": "ja", "javanese": "jw", "kannada": "kn", "korean": "ko", "kurdish": "ku", "latin": "la", "latvian": "lv", "lithuanian": "lt", "malagasy": "mg", "malayalam": "ml", "malaysian": "ms", "mandarin": "zh", "marathi": "mr", "mongolian": "mn", "nepali": "ne", "norwegian": "no", "pashto": "ps", "polish": "pl", "portuguese": "pt", "punjabi": "pa", "romanian": "ro", "russian": "ru", "serbian": "sr", "sesotho": "st", "sinhala": "si", "slovak": "sk", "swahili": "sw", "swedish": "sv", "tagalog": "tl", "tamil": "ta", "telugu": "te", "thai": "th", "tigrinya": "ti", "turkish": "tr", "ukrainian": "uk", "vietnamese": "vi", "welsh": "cy", "xhosa": "xh", "yiddish": "yi", "zulu": "zu" }
waiting_messages = {
    "grammar": [
        "Checking grammar... ✍️",
        "Proofreading your text... 📖",
        "Analyzing sentence structure... 🔍",
        "Ensuring grammatical accuracy... ✅",
    ],
    "translate": [
        "Translating text... 🌍",
        "Processing your translation... 🔄",
        "Finding the right words... 📖",
        "Let's break the language barrier! 💬",
    ],
    "language": [
        "Determining language... 🌍",
        "Figuring out the language code... 🔤",
        "Identifying the language... 📜",
        "Just a moment while we detect the language... 🕒",
    ],
}


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def grammar(ctx, *, text: str):
    message = await ctx.send(random.choice(waiting_messages["grammar"]))

    async def background_task():
        response = await get_ai_response("grammar", text)
        await message.edit(content=response)

    asyncio.create_task(background_task())

@bot.command()
async def translate(ctx, language_pair: str, *, text: str):
    message = await ctx.send(random.choice(waiting_messages["translate"]))

    try:
        source_lang, target_lang = language_pair.split("->")
    except ValueError:
        await message.edit(content="Invalid language pair format! Use the format: [source_lang->target_lang]. Example: `!translate en->fr Hello`")
        return
    
    translated_text = translate_text(text, source_lang, target_lang)
    await message.edit(content=f"**Translated from {source_lang} to {target_lang}:** {translated_text}")


@bot.command()
async def language(ctx, language_name: str):
    message = await ctx.send(random.choice(waiting_messages["language"]))
    language_name = language_name.lower()
    
    if language_name in language_map:
        await message.edit(content=f"The language code for {language_name} is `{language_map[language_name]}`.")
    else:
        await message.edit(content=f"Sorry, I don't have a language code for '{language_name}'. Please check the language name and try again.")



@bot.command()
async def help(ctx, command: str=None):
    if command is None:
        help_message = """
        **MiniMind Commands**:robot: ```ini
!ping - Check if the bot is online 🏓
!help - Show this help message ❓
!grammar <text> - Check for grammar and spelling errors ✍️
!translate <text> - Translate text to English 🌍
!language <language> - Retrieves the language code for the specified language.```"""
        await ctx.send(help_message)
    elif command == "translate":
        translate_help = """
        **!translate Command Help** 🌍
Use this command to translate text to English or other languages.
    
    **Command Format:** `!translate <language_pair> <text>`
        
    **Language Pair Format:** `<source_language_code>-><target_language_code>`

To check for language codes, use the command !language <language> to retrieve the corresponding language code.
"""
        await ctx.send(translate_help)
    elif command == "language":
        language_help = """
        **!language Command Help** 
Use this command to retrieve the language code for a language, which can then be used in the !translate command.

    **Command Format:** `!language <language>`
    *Example: !language english -> en*
"""
        await ctx.send(language_help)
    else:
        await ctx.send("Unknown command. Type `!help` for a list of commands.")


bot.run(TOKEN)
