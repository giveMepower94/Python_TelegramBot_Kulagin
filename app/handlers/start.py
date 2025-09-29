from telegram import Update
from telegram.ext import ContextTypes
from app.calendar_bot import CalendarDB
from app.users import UsersDB
import datetime

users_db = UsersDB()
calendar = CalendarDB()

# Шаги для диалогов
CHOOSING, CREATE_NAME, CREATE_DATE, CREATE_TIME, CREATE_DETAILS = range(5)
READ_ID, DELETE_ID, EDIT_ID, EDIT_FIELD, EDIT_VALUE = range(5, 10)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = users_db.add_user(
        tg_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    if user_id:
        await update.message.reply_text("✅ Вы успешно зарегистрированы!")
    else:
        await update.message.reply_text("ℹ️ Вы уже зарегистрированы.")

    return await start(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = (
        "👋 Привет! Это календарь-бот.\n"
        "Пожалуйста, выберите действие:\n\n"
        "1️⃣ Создать событие\n"
        "2️⃣ Читать событие\n"
        "3️⃣ Удалить событие\n"
        "4️⃣ Список событий за сегодня\n"
        "5️⃣ Редактирование события\n"
        "Напишите цифру действия в ответ на это сообщение."
    )
    await update.message.reply_text(menu_text)
    return CHOOSING


async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    choice = update.message.text.strip()

    if choice == "1":
        await update.message.reply_text("Введите название события:")
        return CREATE_NAME
    elif choice == "2":
        await update.message.reply_text("Введите ID события для чтения:")
        return READ_ID
    elif choice == "3":
        await update.message.reply_text("Введите ID события для удаления:")
        return DELETE_ID
    elif choice == "4":
        user_id = update.effective_user.id
        events = calendar.get_list_event(datetime.date.today().isoformat(), user_id)
        if events:
            text = "\n\n".join(
                [f"{e['id']}: {e['name']} {e['date']} {e['time']} - {e['details']}" for e in events]
            )
            await update.message.reply_text(f"📋 События на сегодня:\n\n{text}")
        else:
            await update.message.reply_text("Сегодня нет событий")
        return await start(update, context)
    elif choice == "5":
        await update.message.reply_text("Введите ID события для редактирования:")
        return EDIT_ID

    else:
        await update.message.reply_text("❌ Неверный выбор. Попробуйте снова.")
        return await start(update, context)


# === Создание события ===
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введите дату события (в формате YYYY-MM-DD):")
    return CREATE_DATE


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        date = datetime.date.fromisoformat(update.message.text)
        context.user_data['date'] = date.isoformat()
        await update.message.reply_text("Введите время события (в формате HH:MM):")
        return CREATE_TIME
    except ValueError:
        await update.message.reply_text("❌ Неверный формат даты. Попробуйте снова (YYYY-MM-DD).")
        return CREATE_DATE


async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        datetime.datetime.strptime(update.message.text, "%H:%M")
        context.user_data['time'] = update.message.text
        await update.message.reply_text("Введите детали события:")
        return CREATE_DETAILS
    except ValueError:
        await update.message.reply_text("❌ Неверный формат времени. Попробуйте еще раз (HH:MM).")
        return CREATE_TIME


async def get_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['details'] = update.message.text
    user_id = update.effective_user.id

    # Проверяем, зарегистрирован ли пользователь
    if not users_db.user_exists(user_id):
        await update.message.reply_text(
            "❌ Сначала зарегистрируйтесь через команду /register"
        )
        return CHOOSING

    event_id = calendar.create_event(
        context.user_data["name"],
        context.user_data["date"],
        context.user_data["time"],
        context.user_data["details"],
        user_id
    )
    await update.message.reply_text(f"✅ Событие создано с ID {event_id} TG_ID {user_id}!")
    return await start(update, context)


# === Чтение события ===
async def read_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        event_id = int(update.message.text)
        user_id = update.effective_user.id
        event = calendar.read_event(event_id, user_id)
        if event:
            await update.message.reply_text(f"📖 Событие:\n\n{event}")
        else:
            await update.message.reply_text("❌ Событие с таким ID не найдено.")
    except ValueError:
        await update.message.reply_text("❌ Введите число (ID события).")
    return await start(update, context)


# === Удаление события ===
async def delete_event_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        event_id = int(update.message.text)
        user_id = update.effective_user.id
        deleted = calendar.delete_event(event_id, user_id)
        if deleted:
            await update.message.reply_text(f"🗑 Событие с ID {event_id} удалено.")
        else:
            await update.message.reply_text("❌ Событие с таким ID не найдено.")
    except ValueError:
        await update.message.reply_text("❌ Введите число (ID события).")
    return await start(update, context)


# === Редактирование события ===
async def edit_event_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        event_id = int(update.message.text)
        context.user_data['event_id'] = event_id
        await update.message.reply_text(
            "Что вы хотите изменить?\n"
            "Введите одно из: name, date, time, details"
        )
        return EDIT_FIELD
    except ValueError:
        await update.message.reply_text("❌ Введите число (ID события).")
        return await start(update, context)


async def edit_event_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    field = update.message.text.strip().lower()
    if field not in ['name', 'date', 'time', 'details']:
        await update.message.reply_text(
            "❌ Неверное поле. Введите name, date, time или details."
        )
        return EDIT_FIELD
    context.user_data["edit_field"] = field
    await update.message.reply_text(f"Введите новое значение для {field}:")
    return EDIT_VALUE


async def edit_event_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    event_id = context.user_data['event_id']
    field = context.user_data["edit_field"]
    value = update.message.text
    user_id = update.effective_user.id

    success = calendar.edit_event(
        event_id,
        user_id,
        **{field: value}
    )

    if success:
        await update.message.reply_text(f"✅ Событие {event_id} обновлено (поле {field}).")
    else:
        await update.message.reply_text("❌ Событие не найдено.")
    return await start(update, context)
