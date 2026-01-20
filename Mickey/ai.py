import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are a funny, desi, Hinglish-speaking Telegram chatbot. "
    "You reply smartly, lightly roast users, no abuse, no NSFW."
)

def get_ai_reply(user_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.8,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
