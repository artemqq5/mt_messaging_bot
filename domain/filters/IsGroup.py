from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.repositories.AdminRepository import AdminRepository


class IsGropFilter(BaseFilter):

    def __init__(self, m: bool = True):
        self.m = m

    async def __call__(self, message: Message):
        is_group = message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
        if self.m:
            return is_group
        else:
            return not is_group

