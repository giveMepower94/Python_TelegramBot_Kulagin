import logging
from telegram.ext import Application, CommandHandler
from secret import API_TOKEN
from app.handlers.start import start


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = API_TOKEN


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
