from telegram import Update
import logging
from telegram.ext import ContextTypes, ConversationHandler
from note import delete_note, read_note, edit_note

ASK_READ_NAME, ASK_DELETE_NAME, ASK_EDIT_NAME, ASK_EDIT_TEXT = range(4)


async def start_read(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите название заметки для чтения")
    return ASK_READ_NAME


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


async def start_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите название заметки для удаления!")
    return ASK_DELETE_NAME


async def delete_note_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note_delete = update.message.text
    try:
        rev_note = delete_note(note_delete)
        if rev_note:
            await update.message.reply_text("Заметка успешно удалена!")
        else:
            await update.message.reply_text("Такой заметки нет")
    except Exception as e:
        logging.error(f"Файл не удалился, ошибка {e}")
        await update.message.reply_text("Произошла ошибка при чтении заметки.")
    return ConversationHandler.END


async def start_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите название заметки для редактирования!")
    return ASK_EDIT_NAME


async def edit_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name_note'] = update.message.text
    await update.message.reply_text("Введите текст для редактирования")
    return ASK_EDIT_TEXT


async def edit_note_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note_name = context.user_data['name_note']
    new_text = update.message.text
    try:
        success = edit_note(note_name, new_text)
        if success:
            await update.message.reply_text(f"Заметка '{note_name}' обновлена.")
        else:
            await update.message.reply_text("Такой заметки нет.")
    except Exception as e:
        logging.error(f"Ошибка при редактировании - {e}")
        await update.message.reply_text("Произошла ошибка при редактировании заметки.")
    return ConversationHandler.END

