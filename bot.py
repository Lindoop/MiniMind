# Library Import
import discord  
import asyncio
import random
import os
import threading

# Discord Library Import
from discord.ext import commands

# Environment Variables Fetch
from flask import Flask
from dotenv import load_dotenv

# Functions File Import
from functions import get_ai_response
from functions import translate_text

load_dotenv(dotenv_path='minimind.env')
TOKEN = os.getenv('DISCORD_TOKEN')

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
    "summarize": [
        "Summarizing your text... 📝",
        "Breaking it down... 🔍",
        "Giving you the highlights... 🌟",
        "Compressing your text... 💼",
    ],
    "synonym": [
        "Finding the perfect match... 🔍",
        "Fetching synonyms... 📚",
        "Digging up synonyms... 🌱",
        "Exploring word options... 🧠",
    ]
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
async def summarize(ctx, *, text: str):
    message = await ctx.send(random.choice(waiting_messages["summarize"]))
    
    async def background_task():
        response = await get_ai_response("summarize", text)
        await message.edit(content=f"**Paraphrased Text:** {response}")
    
    asyncio.create_task(background_task())


@bot.command()
async def dictionary(ctx, word: str):
    message = await ctx.send(random.choice(waiting_messages["dictionary"]))

    response = await get_ai_response("dictionary", word)
    await message.edit(content=f"**Definition of '{word}':**\n{response}")


@bot.command()
async def synonym(ctx, word: str):
    message = await ctx.send(random.choice(waiting_messages["synonym"]))

    response = await get_ai_response("synonym", word)
    await message.edit(content=f"**Synonyms for '{word}':**\n{response}")


@bot.command()
async def help(ctx, command: str=None):
    if command is None:
        help_message = """
        **MiniMind Commands**:robot: ```ini
!ping - Check if the bot is online 🏓
!help - Show this help message ❓
!grammar <text> - Check for grammar and spelling errors ✍️
!translate <text> - Translate text to English 🌍
!language <language> - Retrieves the language code for the specified language.
!summarize <text> - Condenses long text into a short summary.```"""
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

def home():
    return "I'm alive! 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()

keep_alive

bot.run(TOKEN)