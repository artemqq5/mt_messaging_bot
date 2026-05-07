from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, types
from aiogram.enums import ChatType
from aiogram.types import TelegramObject

from bot.data.repositories.AdminRepository import AdminRepository
from bot.data.repositories.UserRepository import UserRepository


class IsGroupUser(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, (types.Message, types.CallbackQuery)):
            return

        chat = event.message.chat if isinstance(event, types.CallbackQuery) else event.chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            return
        if await AdminRepository.is_admin(event.from_user.id):
            return
        if await UserRepository.is_user(event.from_user.id):
            return

        return await handler(event, data)
