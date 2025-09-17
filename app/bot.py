import logging
from app.note import build_note
from telegram.ext import (Application, CommandHandler, MessageHandler,
                          ConversationHandler, filters)
from secret import API_TOKEN
from app.handlers.create import (ASK_NAME, ASK_TEXT, start_create, get_name,
                                 cancel_note, get_text)
from app.handlers.read_edit_delete import (
    ASK_READ_NAME, ASK_DELETE_NAME, ASK_EDIT_NAME, ASK_EDIT_TEXT,
    start_read, read_note_handler,
    delete_note_handler, start_delete,
    start_edit, edit_note_handler, edit_text_handler
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

TOKEN = API_TOKEN


def main():
    app = Application.builder().token(TOKEN).build()

    # === CREATE HANDLER ===
    create_conv = ConversationHandler(
        entry_points=[CommandHandler("create", start_create)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ASK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_text)],
        },
        fallbacks=[CommandHandler("cancel", cancel_note)]
    )

    # === READ ===
    read_conv = ConversationHandler(
        entry_points=[CommandHandler("read", start_read)],
        states={
            ASK_READ_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, read_note_handler)],
        },
        fallbacks=[]
    )

    # === DELETE ===
    delete_conv = ConversationHandler(
        entry_points=[CommandHandler("delete", start_delete)],
        states={
            ASK_DELETE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_note_handler)]
        },
        fallbacks=[]
    )

    # === EDIT ===
    edit_conv = ConversationHandler(
        entry_points=[CommandHandler("edit", start_edit)],
        states={
            ASK_EDIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_text_handler)],
            ASK_EDIT_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_note_handler)],
        },
        fallbacks=[]
    )

    app.add_handler(create_conv)
    app.add_handler(read_conv)
    app.add_handler(delete_conv)
    app.add_handler(edit_conv)

    app.run_polling()
