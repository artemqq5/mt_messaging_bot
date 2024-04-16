from aiogram.fsm.state import StatesGroup, State


class SendMessageState(StatesGroup):
    category = State()
    message = State()
    button = State()
    buttonText = State()
    buttonUrl = State()
    photo = State()
    preview = State()

