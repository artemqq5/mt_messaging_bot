from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.repositories.ChatRepository import ChatRepository
from domain.filters.IsAdmin import IsAdminFilter
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



