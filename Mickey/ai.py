import google.generativeai as genai
from config import GEMINI_API_KEY
import asyncio

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

async def get_ai_reply(text):
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model.generate_content(text)
        )
        return response.text
    except Exception:
        return "⚠️ AI error, try again"
