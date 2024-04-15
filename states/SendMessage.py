from aiogram.fsm.state import StatesGroup, State


class SendMessageState(StatesGroup):
    category = State()
    message = State()
    photo = State()
    preview = State()

