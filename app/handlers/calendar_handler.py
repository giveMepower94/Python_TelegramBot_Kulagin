from telegram.ext import MessageHandler, filters, ContextTypes
from telegram import Update


async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip()

    if choice == "1":
        await update.message.reply_text("Вы выбрали: Создать событие 📝")
    elif choice == "2":
        await update.message.reply_text("Вы выбрали: Читать событие 📖")
    elif choice == "3":
        await update.message.reply_text("Вы выбрали: Редактировать событие ✏️")
    elif choice == "4":
        await update.message.reply_text("Вы выбрали: Удалить событие ❌")
    elif choice == "5":
        await update.message.reply_text("Вы выбрали: Список событий за сегодня 📋")
    else:
        await update.message.reply_text("❌ Некорректный выбор. Введите цифру от 1 до 5.")