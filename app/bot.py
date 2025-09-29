import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from secret import API_TOKEN
from app.handlers.start import (
    start, handle_choice, register,
    CHOOSING,
    CREATE_NAME, CREATE_DATE, CREATE_TIME, CREATE_DETAILS,
    get_name, get_date, get_time, get_details,
    READ_ID, DELETE_ID, EDIT_ID, EDIT_FIELD, EDIT_VALUE,
    read_event_handler, delete_event_handler,
    edit_event_start, edit_event_field, edit_event_value
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = API_TOKEN


def main():
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            CREATE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CREATE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            CREATE_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
            CREATE_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],

            READ_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, read_event_handler)],
            DELETE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_event_handler)],

            EDIT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_event_start)],
            EDIT_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_event_field)],
            EDIT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_event_value)],
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("register", register))
    app.run_polling()


if __name__ == "__main__":
    main()
