from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMessage(StatesGroup):
    message = State()
    photo = State()
    check = State()
