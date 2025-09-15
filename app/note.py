import re
import os
import os.path


# Создайте функцию, которая создает заметку по запросу пользователя
def build_note(note_text, note_name):
    # Проверьте, существует ли файл, название которого указывает пользователь.
    # Если нет, создайте новый файл. Если да, замените существующий файл на новый.
    try:
        try:
            file = open(f"{note_name}.txt", "r+", encoding="utf-8")
            print("Такой файл существует")
        except IOError:
            file = open(f"{note_name}.txt", "w+", encoding="utf-8")
            print("Файл создан")
        file.write(note_text)
        print(f"Заметка {note_name} создана.")
    except Exception as e:
        print(f"Что-то пошло не так, ошибка {e}")


# Напишите функцию, которая запрашивает название и текст заметки, а затем создает ее
def create_note():
    # Создайте файл с заметкой
    try:
        # Запросите название заметки и проверьте его на наличие запрещенных символов
        note_name = input("Введите название заметки: ")
        forbidden_symbols = "\\|/*<>?:"  # набор запрещенных символов для Windows
        pattern = "[{0}]".format(forbidden_symbols)
        if re.search(pattern, note_name):
            print(
                "Вы ввели недопустимые символы в названии файла. Переименуйте заметку."
            )
        # Запросите текст заметки и создайте заметку
        else:
            print("Название заметки создано.")
            note_text = input("Введите текст заметки: ")
            build_note(note_text, note_name)
    except Exception as e:
        print(f"Что-то пошло не так, ошибка {e}")


# Напишите функцию, которая прочитает заметку и выведет ее текст
def read_note(note_name: str) -> None:
    """Читает заметку по названию. Возвращает текст или None, если нет файла"""
    try:
        path = f"{note_name}.txt"
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            None
    except Exception as e:
        print(f"Не смогли прочитать, ошибка: {e}")


def edit_note(note_name: str, new_text: str) -> bool:
    """Редактирует заметку. Возвращает True, если успешно, иначе False."""
    try:
        path = f"{note_name}.txt"
        if os.path.isfile(path):
            with open(path, 'w', encoding="utf-8") as file:
                file.write(new_text)
            return True
        else:
            return False
    except Exception:
        return False


def delete_note(note_name: str) -> bool:
    """Удаляет заметку. Возвращает True, если удалена, иначе False."""
    try:
        path = f"{note_name}.txt"
        if os.path.isfile(path):
            os.remove(path)
            return True
        else:
            return False
    except Exception:
        return False


# Напишите функцию, которая выведет все заметки пользователя в порядке от самой короткой до самой длинной
def display_notes():
    try:
        notes = [note for note in os.listdir() if note.endswith(".txt")]
        sorted_notes = sorted(notes, key=len, reverse=True)
        print(
            "Это список всех заметок в порядке от самой короткой до самой длинной: \n",
            sorted_notes,
        )
    except Exception as e:
        print(f"Что-то пошло не так, ошибка {e}")


# Напишите функцию, которая выведет все заметки пользователя в порядке от самой длинной до самой короткой
def display_sorted_notes():
    try:
        notes = [note for note in os.listdir() if note.endswith(".txt")]
        sorted_list = sorted(notes, key=len)
        print(
            "\nЭто список заметок в порядке от самой длинной до самой короткой: \n",
            sorted_list,
        )
    except Exception as e:
        print(f"Что-то пошло не так, ошибка {e}")


# Создайте функцию, которая управляет всеми операциями с заметками
def main():
    # Создайте бесконечный цикл работы с заметками и настройте меню для пользователя
    while True:
        action = input(
            "Нажмите цифру, чтобы выбрать действие, которое хотите выполнить с заметками: "
            "\n"
            "Введите 1, чтобы создать заметку с определенным названием и текстом."
            "\n"
            "Введите 2, чтобы вывести на экран нужную вам заметку."
            "\n"
            "Введите 3, чтобы отредактировать нужную вам заметку."
            "\n"
            "Введите 4, чтобы удалить заметку."
            "\n"
            "Введите 5, чтобы вывести все заметки в порядке от самой короткой до самой длинной."
            "\n"
            "Введите 6, чтобы вывести все заметки в порядке от самой длинной до самой короткой."
            "\n"
            "Введите n, чтобы выйти из приложения."
            "\n"
            "Что вы хотите сделать?"
        ).lower()
        # Проверьте символ, который ввел пользователь. Если он некорректный, сообщите об этом.
        allowed_symbols = "123456n"
        pattern1 = "[{0}]".format(allowed_symbols)
        if re.search(pattern1, action):
            print("Вы ввели корректный запрос. Действие сейчас выполнится.")
            if action == "1":
                create_note()
            if action == "2":
                read_note()
            if action == "3":
                edit_note()
            if action == "4":
                delete_note()
            if action == "5":
                display_notes()
            if action == "6":
                display_sorted_notes()
            if action == "n":
                break
        else:
            print(
                "Вы ввели некорректный символ. Пожалуйста, введите цифры от 1 до 6 или n."
            )

        # Предложите пользователю продолжить работу с приложением
        print("Чтобы продолжить работать с заметками, нажмите y/n")
        answer = input().lower()
        if answer != "y":
            break


main()
