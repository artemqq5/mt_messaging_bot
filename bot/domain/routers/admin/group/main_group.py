import logging
from datetime import datetime

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.data.repositories.ChatRepository import ChatRepository
from bot.domain.filters.IsGroup import IsGropFilter
from bot.domain.middlewares.IsGroupAdmin import IsGroupAdmin
from bot.domain.routers.admin.group.menu import update_

router = Router()
router.include_routers(
    update_.router
)

router.message.middleware(IsGroupAdmin())
router.callback_query.middleware(IsGroupAdmin())


@router.message(F.migrate_to_chat_id)
async def handle_migration(message: Message):
    updated = await ChatRepository.update_group_id(message.chat.id, message.migrate_to_chat_id)
    logging.info(f"group migration: {message.chat.id} → {message.migrate_to_chat_id}, updated={updated}")


@router.message(Command("start"), IsGropFilter())
async def start(message: types.Message, state: FSMContext):
    if await ChatRepository.add_chat(group_id=message.chat.id, title=message.chat.title, datetime=datetime.now()):
        await message.answer("Group added, set status")
    else:
        await message.answer("Error or the group was added earlier, please try to set the status")
