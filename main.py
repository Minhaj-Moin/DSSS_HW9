## TO RUN ON GOOGLE COLAB
#!pip install -q python-telegram-bot
from telegram import Update
import requests
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
#from google.colab import userdata
import os

# TELEGRAM_API_KEY = userdata.get('TELEGRAM_API_KEY')
TELEGRAM_API_KEY = os.environ['TELEGRAM_API_KEY']
# GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! MinhajBot here, how can I help you?")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json_data = {'contents': [{'parts': [{'text': update.message.text}]}]}
    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        params={'key': GOOGLE_API_KEY},
        headers={'Content-Type': 'application/json'},
        json=json_data)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response.json()['candidates'][0]['content']['parts'][0]['text'])


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()
