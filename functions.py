import google.generativeai as genai
import language_tool_python
from deep_translator import GoogleTranslator
import time
import os
import asyncio

from dotenv import load_dotenv
load_dotenv(dotenv_path='minimind.env')

API_KEY = os.getenv('API_KEY')

genai.configure(api_key=API_KEY)

async def get_ai_response(task: str, text: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        prompt = ""

        if task == "grammar":
            prompt = f"Check for grammar and spelling errors. Return a grammatically correct version of the text:\n\n{text}"
        elif task == "summarize":
            prompt = f"Summarize the following text. Return a concise version capturing the highlights of the text:\n\n{text}"
        else:
            prompt = text

        #gen_start = time.time()
        response = await asyncio.to_thread(model.generate_content, prompt)
        #print(f"[{time.time() - gen_start:.2f}s] AI generation took")

        return response.text if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        print(f"❌ Error in AI request: {e}")
        return f"Error: {e}"
    
    

def translate_text(text: str, source_language: str, target_language: str) -> str:
    try:
        translator = GoogleTranslator(source=source_language, target=target_language)
        return translator.translate(text)
    except Exception as e:
        return f"Error: {e}"