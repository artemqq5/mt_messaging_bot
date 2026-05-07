import logging
from typing import Optional

from sqlalchemy import delete, select, update

from bot.data.db_connection import async_session, log_exc_with_try_except
from bot.data.models import AdminModel
from bot.data.other.accesses import TypeOfAdmins


class AdminRepository:

    @staticmethod
    @log_exc_with_try_except()
    async def is_admin(telegram_id) -> Optional[AdminModel]:
        async with async_session() as session:
            result = await session.execute(
                select(AdminModel).where(AdminModel.telegram_id == str(telegram_id)).limit(1)
            )
            return result.scalar_one_or_none()

    @staticmethod
    @log_exc_with_try_except()
    async def get_admins() -> list[AdminModel] | None:
        async with async_session() as session:
            result = await session.execute(
                select(AdminModel).where(AdminModel.role == TypeOfAdmins.ADMIN.value)
            )
            return result.scalars().all()

    @staticmethod
    @log_exc_with_try_except()
    async def get_all_admins() -> list[AdminModel] | None:
        async with async_session() as session:
            result = await session.execute(select(AdminModel))
            return result.scalars().all()

    @staticmethod
    async def add_admin(telegram_id: str, name: str, role: str) -> Optional[AdminModel]:
        try:
            async with async_session() as session:
                async with session.begin():
                    admin = AdminModel(telegram_id=str(telegram_id), name=name, role=role)
                    session.add(admin)
                    await session.flush()
                    await session.refresh(admin)
                    session.expunge(admin)
                    return admin
        except Exception as e:
            logging.error(f"[AdminRepository] add_admin error: {e}")
            return None

    @staticmethod
    async def remove_admin(telegram_id: str) -> bool:
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        delete(AdminModel).where(AdminModel.telegram_id == str(telegram_id))
                    )
                    return result.rowcount > 0
        except Exception as e:
            logging.error(f"[AdminRepository] remove_admin error: {e}")
            return False

    @staticmethod
    async def update_admin_role(telegram_id: str, role: str) -> bool:
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        update(AdminModel)
                        .values(role=role)
                        .where(AdminModel.telegram_id == str(telegram_id))
                    )
                    return result.rowcount > 0
        except Exception as e:
            logging.error(f"[AdminRepository] update_admin_role error: {e}")
            return False
