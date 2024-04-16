from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.repositories.ChatRepository import ChatRepository
from domain.filters.IsGroup import IsGropFilter
from domain.middlewares.IsGroupAdmin import IsGroupAdmin
from domain.middlewares.IsPrivateChatAdmin import IsPrivateChatAdmin
from domain.routers.admin.group.menu import update_
from presentation.keyboard.admin_ import kb_main

router = Router()
router.include_routers(
    update_.router
)

router.message.middleware(IsGroupAdmin())
router.callback_query.middleware(IsGroupAdmin())


@router.message(Command("start"), IsGropFilter())
async def start(message: types.Message, state: FSMContext):
    if ChatRepository().add_chat(group_id=message.chat.id, title=message.chat.title, datetime=datetime.now()):
        await message.answer("Група додана, встановіть статус")
    else:
        await message.answer("Помилка або група додана раніше, спробуйте встановити статус")

