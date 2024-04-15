from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message

from data.other.constants import *
from data.repositories.AdminRepository import AdminRepository
from data.repositories.ChatRepository import ChatRepository
from domain.filters.IsAdmin import IsAdminFilter
from domain.middlewares.IsPrivateChatAdmin import IsPrivateChatAdmin
from presentation.keyboard.admin_ import kb_main, kb_cancel

router = Router()


@router.message(
    Command("agency_fb", "agency_google", "apps", "google", "fb", "creo", "console", "pp_web", "pp_ads", "media"))
async def update_chat(message: Message, state: FSMContext):
    chat_type = message.text.split(' ')[0].replace("/", "")
    chat_type = chat_type.split("@")[0] if chat_type.__contains__("@") else chat_type
    available = 0
    try:
        update_available = int(message.text.split(' ')[1])
        if update_available in (0, 1):
            available = update_available
    except Exception as e:
        print(f"exception update {e}")

    if ChatRepository().update_chat_type(message.chat.id, chat_type, available):
        await message.answer(f"Група оновила статус {chat_type} на {available}")
    else:
        await message.answer(f"Помилка при оновленні статусу")
