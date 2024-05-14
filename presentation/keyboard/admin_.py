import math

from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from data.other.accesses import access_admin_to_chat, TypeOfAdmins
from data.other.constants import VIEW_ALL_GROUP, MESSAGING_GROP, CANCEL, SKIP, SEND, BUG_REPORT, \
    UNSPECIFIED_GROUPS, STATISTIC, YES


def kb_type_group(admin) -> ReplyKeyboardBuilder:
    keyboard = []

    if admin['role'] == TypeOfAdmins.ADMIN.value:
        keyboard.append([KeyboardButton(text=UNSPECIFIED_GROUPS)])

    for chat in access_admin_to_chat[admin['role']]:
        keyboard.append([KeyboardButton(text=chat)])

    keyboard.append([KeyboardButton(text=CANCEL)])

    return ReplyKeyboardBuilder(keyboard)


def kb_messaging_category(admin) -> ReplyKeyboardBuilder:
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
    [KeyboardButton(text=MESSAGING_GROP)],
    [KeyboardButton(text=BUG_REPORT)],
    [KeyboardButton(text=STATISTIC)]
])

kb_quetion = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=YES)],
    [KeyboardButton(text=SKIP)],
    [KeyboardButton(text=CANCEL)]
])

kb_send = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=SEND)],
    [KeyboardButton(text=CANCEL)]
])


class GroupCallback(CallbackData, prefix="group*callback"):
    id: str


class GroupPageCallback(CallbackData, prefix="group*page*callback"):
    page: int


def kb_groups(groups) -> InlineKeyboardBuilder:
    markup = []
    for group in groups:
        markup.append(
            [InlineKeyboardButton(text=group['title'], callback_data=GroupCallback(id=group['group_id']).pack())]
        )
    return InlineKeyboardBuilder(markup=markup)


def generate_pagination_groups(current_page: int, groups) -> InlineKeyboardBuilder:
    total_pages = math.ceil(len(groups)/10)
    keyboard = []

    start_index = (current_page - 1) * 10
    end_index = min(start_index + 10, len(groups))

    for i in range(start_index, end_index):
        keyboard.append([InlineKeyboardButton(
            text=groups[i]['title'],
            callback_data=GroupCallback(id=groups[i]['group_id']).pack()
        )])

    # Navigation buttons
    if current_page > 1:
        keyboard.append([InlineKeyboardButton(
            text='<< Назад',
            callback_data=GroupPageCallback(page=current_page - 1).pack()
        )])
    if current_page < total_pages:
        keyboard.append([InlineKeyboardButton(
            text='Вперед >>',
            callback_data=GroupPageCallback(page=current_page + 1).pack()
        )])

    return InlineKeyboardBuilder(markup=keyboard)
