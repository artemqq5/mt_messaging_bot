from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from role.accesses import TypeOfAdmins, access_admin_to_chat


def chat_type_category(admin) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup()

    for chat in access_admin_to_chat[admin['role']]:
        keyboard.add((KeyboardButton(text=chat)))

    return keyboard
