from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from note import build_note

ASK_NAME, ASK_TEXT = range(2)


async def start_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите название заметки")
    return ASK_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['note_name'] = update.message.text
    await update.message.reply_text("Введите текст заметки")
    return ASK_TEXT


async def get_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    n_name = context.user_data['note_name']
    n_text = update.message.text

    try:
        build_note(n_text, n_name)
        await update.message.reply_text("Заметка успешно создана")
    except Exception as e:
        await update.message.reply_text(f"Заметку создать не удалось, ошибка {e}")
    return ConversationHandler.END


async def cancel_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Создать заметку не получилось")
    return ConversationHandler.END
