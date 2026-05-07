from typing import Optional

from sqlalchemy import func, select, desc

from bot.data.db_connection import async_session, log_exc_with_try_except
from bot.data.models import UserModel


class UserRepository:

    @staticmethod
    @log_exc_with_try_except()
    async def is_user(user_id) -> Optional[UserModel]:
        async with async_session() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.user_id == str(user_id)).limit(1)
            )
            return result.scalar_one_or_none()

    @staticmethod
    @log_exc_with_try_except()
    async def add_user(user_id, username, group_id, time, first_name, lang_code, chat_name, link_group) -> Optional[UserModel]:
        async with async_session() as session:
            async with session.begin():
                user = UserModel(
                    user_id=str(user_id),
                    username=username,
                    group_id=str(group_id),
                    time=time,
                    first_name=first_name,
                    language_code=lang_code,
                    title_group=chat_name,
                    link_group=link_group,
                )
                session.add(user)
                await session.flush()
                await session.refresh(user)
                session.expunge(user)
                return user

    @staticmethod
    @log_exc_with_try_except()
    async def get_users() -> list[UserModel] | None:
        async with async_session() as session:
            result = await session.execute(select(UserModel))
            return result.scalars().all()

    @staticmethod
    @log_exc_with_try_except()
    async def count_users_total() -> int:
        async with async_session() as session:
            result = await session.execute(select(func.count()).select_from(UserModel))
            return result.scalar_one() or 0

    @staticmethod
    @log_exc_with_try_except()
    async def count_users_in_group(group_id: str) -> int:
        async with async_session() as session:
            result = await session.execute(
                select(func.count()).where(UserModel.group_id == str(group_id))
            )
            return result.scalar_one() or 0

    @staticmethod
    @log_exc_with_try_except()
    async def top_groups_by_users(limit: int = 5):
        async with async_session() as session:
            result = await session.execute(
                select(UserModel.group_id, UserModel.title_group, func.count().label("cnt"))
                .group_by(UserModel.group_id, UserModel.title_group)
                .order_by(desc("cnt"))
                .limit(limit)
            )
            return result.all()
