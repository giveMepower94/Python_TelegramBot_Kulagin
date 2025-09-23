from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = (
        "👋 Привет! Это календарь-бот.\n"
        "Пожалуйста, выберите действие:\n\n"
        "1️⃣ Создать событие\n"
        "2️⃣ Читать событие\n"
        "3️⃣ Редактировать событие\n"
        "4️⃣ Удалить событие\n"
        "5️⃣ Список событий за сегодня\n\n"
        "Напишите цифру действия в ответ на это сообщение."
    )
    await update.message.reply_text(menu_text)
