from aiogram.fsm.state import StatesGroup, State


class SendMessageState(StatesGroup):
    category = State()
    message = State()
    button = State()
    buttonText = State()
    buttonUrl = State()
    buttonRepeat = State()
    photo = State()
    preview = State()

