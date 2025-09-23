import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from secret import API_TOKEN
from app.handlers.start import start
from app.handlers.calendar_handler import handle_choice


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = API_TOKEN


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice))
    app.run_polling()


if __name__ == "__main__":
    main()
