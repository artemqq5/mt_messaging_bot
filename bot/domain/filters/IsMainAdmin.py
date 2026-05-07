from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.data.other.accesses import TypeOfAdmins
from bot.data.repositories.AdminRepository import AdminRepository


class IsMainAdminFilter(BaseFilter):
    async def __call__(self, message: Message):
        admin = await AdminRepository.is_admin(message.from_user.id)
        return admin is not None and admin.role == TypeOfAdmins.ADMIN.value
