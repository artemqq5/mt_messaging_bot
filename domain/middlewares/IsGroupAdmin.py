from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, types
from aiogram.enums import ChatType
from aiogram.types import TelegramObject

from data.repositories.AdminRepository import AdminRepository


class IsGroupAdmin(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, (types.Message, types.CallbackQuery)):
            return

        if event.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP] or not AdminRepository().is_admin(
                event.from_user.id):
            return

        return await handler(event, data)
