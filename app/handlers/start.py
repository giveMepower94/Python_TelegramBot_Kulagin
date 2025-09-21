from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📅 Создать"), KeyboardButton("📖 Читать")],
        [KeyboardButton("✏️ Редактировать"), KeyboardButton("❌ Удалить")],
        [KeyboardButton("📋 Список за сегодня")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Привет! Это календарь-бот.\n"
        "Пожалуйста, выберите действие:",
        reply_markup=reply_markup
    )
