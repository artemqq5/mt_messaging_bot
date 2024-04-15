from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from data.other.accesses import access_admin_to_chat
from data.other.constants import VIEW_ALL_GROUP, MESSAGING_GROP, CANCEL, SKIP, SEND


def kb_access_category(admin) -> ReplyKeyboardBuilder:
    keyboard = []

    for chat in access_admin_to_chat[admin['role']]:
        keyboard.append([KeyboardButton(text=chat)])

    keyboard.append([KeyboardButton(text=CANCEL)])

    return ReplyKeyboardBuilder(keyboard)


kb_cancel = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=CANCEL)]
])

kb_skip = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=SKIP)],
    [KeyboardButton(text=CANCEL)]
])

kb_main = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=VIEW_ALL_GROUP)],
    [KeyboardButton(text=MESSAGING_GROP)]
])

kb_send = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=SEND)],
    [KeyboardButton(text=CANCEL)]
])

# kb_type_group = ReplyKeyboardBuilder(markup=[
#     [KeyboardButton(text=VIEW_ALL_GROUP)],
#     [KeyboardButton(text=VIEW_ALL_GROUP)],
#     [KeyboardButton(text=VIEW_ALL_GROUP)],
#     [KeyboardButton(text=VIEW_ALL_GROUP)],
# ])
#
#
# class GroupCalback(CallbackData, prefix="group*callback"):
#     id: str
#
#
# def kb_groups(groups) -> InlineKeyboardBuilder:
#     markup = []
#     for group in groups:
#         markup.append(
#             [InlineKeyboardButton(text=group['title'], callback_data=GroupCalback(id=group['group_id']).pack())]
#         )
#     return InlineKeyboardBuilder(markup=markup)
