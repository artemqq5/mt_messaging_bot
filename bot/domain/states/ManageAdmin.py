from aiogram.fsm.state import StatesGroup, State


class ManageAdminState(StatesGroup):
    telegram_id = State()
    name = State()
    role = State()
