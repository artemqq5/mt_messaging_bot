from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from data.other.accesses import access_admin_to_chat, TypeOfAdmins
from data.other.constants import VIEW_ALL_GROUP, MESSAGING_GROP, CANCEL, SKIP, SEND, BUG_REPORT, ALL_GROUPS, \
    UNSPECIFIED_GROUPS, STATISTIC


def kb_type_group(admin) -> ReplyKeyboardBuilder:
    keyboard = []

    if admin['role'] == TypeOfAdmins.ADMIN.value:
        keyboard.append([KeyboardButton(text=UNSPECIFIED_GROUPS)])
        keyboard.append([KeyboardButton(text=ALL_GROUPS)])

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
    [KeyboardButton(text=MESSAGING_GROP)],
    [KeyboardButton(text=BUG_REPORT)],
    [KeyboardButton(text=STATISTIC)]
])

kb_send = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=SEND)],
    [KeyboardButton(text=CANCEL)]
])


class GroupCalback(CallbackData, prefix="group*callback"):
    id: str


def kb_groups(groups) -> InlineKeyboardBuilder:
    markup = []
    for group in groups:
        markup.append(
            [InlineKeyboardButton(text=group['title'], callback_data=GroupCalback(id=group['group_id']).pack())]
        )
    return InlineKeyboardBuilder(markup=markup)
