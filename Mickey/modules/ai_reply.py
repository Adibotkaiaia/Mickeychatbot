from pyrogram import Client, filters
import openai
import config
from Mickey import LOGGER

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY

@Client.on_message(filters.text & ~filters.bot)
async def ai_reply(client, message):
    """
    AI reply handler for both private and group messages.
    """
    try:
        # Optional: group me sirf bot mention pe reply
        if message.chat.type in ["group", "supergroup"]:
            if f"@{client.me.username}" not in message.text:
                return  # ignore if bot not mentioned

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a funny, friendly Telegram chatbot who replies in Hinglish."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.8,
            max_tokens=250
        )

        reply_text = response['choices'][0]['message']['content']

        # Send AI reply
        await message.reply_text(reply_text)

    except Exception as e:
        LOGGER.warning(f"AI reply failed: {e}")
        await message.reply_text("⚠️ AI reply failed, try again!")
