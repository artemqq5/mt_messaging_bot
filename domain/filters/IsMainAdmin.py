from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.other.accesses import TypeOfAdmins
from data.repositories.AdminRepository import AdminRepository


class IsMainAdminFilter(BaseFilter):
    async def __call__(self, message: Message):
        return AdminRepository().is_admin(message.chat.id)['role'] == TypeOfAdmins.ADMIN.value
