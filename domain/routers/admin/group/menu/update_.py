from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.repositories.ChatRepository import ChatRepository

router = Router()


@router.message(
    Command("agency_fb", "agency_google", "apps", "google", "shop_fb", "creo", "console", "affiliate_mp", "partner_mp", "media_mt", "media_mp", "partner_mt"))
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
        await message.answer(f"The group updated its status {chat_type} on {available}")
    else:
        await message.answer(f"Error updating the status, maybe you are changing to the same one")
