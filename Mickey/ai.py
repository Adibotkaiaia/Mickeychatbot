import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

async def get_ai_reply(text):
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        return "⚠️ AI error, try again"
