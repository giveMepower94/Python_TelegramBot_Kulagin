from telegram import Update
import logging
from telegram.ext import ContextTypes, ConversationHandler
from note import delete_note, read_note, edit_note

ASK_NAME = 0


async def start_read(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите название заметки для чтения")
    return ASK_NAME


async def read_note_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note_name = update.message.text
    try:
        text = read_note(note_name)
        if text:
            await update.message.reply_text(f"Заметка '{note_name}':\n{text}")
        else:
            await update.message.reply_text("Такой заметки нет")
    except Exception as e:
        logging.error(f"Файл не прочитался, ошибка {e}")
        await update.message.reply_text("Произошла ошибка при чтении заметки.")
    return ConversationHandler.END
