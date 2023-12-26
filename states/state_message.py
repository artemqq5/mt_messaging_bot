from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMessage(StatesGroup):
    category = State()
    message = State()
    photo = State()
    check = State()
