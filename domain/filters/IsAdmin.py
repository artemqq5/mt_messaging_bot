from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.repositories.AdminRepository import AdminRepository


class IsAdminFilter(BaseFilter):

    def __init__(self, is_admin: bool = True):
        self.is_admin = is_admin

    async def __call__(self, message: Message):
        if self.is_admin:
            return AdminRepository().is_admin(message.from_user.id) is not None
        else:
            return AdminRepository().is_admin(message.from_user.id) is None
