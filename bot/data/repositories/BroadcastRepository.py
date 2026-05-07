from datetime import datetime
from typing import Optional

from sqlalchemy import desc, select

from bot.data.db_connection import async_session, log_exc_with_try_except
from bot.data.models import BroadcastModel


class BroadcastRepository:

    @staticmethod
    @log_exc_with_try_except()
    async def add_broadcast(
        admin_id: str,
        admin_name: str,
        category: str,
        message_text: str,
        has_photo: bool,
        has_buttons: bool,
        groups_count: int,
    ) -> Optional[BroadcastModel]:
        async with async_session() as session:
            async with session.begin():
                record = BroadcastModel(
                    admin_id=str(admin_id),
                    admin_name=admin_name,
                    category=category,
                    message_text=message_text,
                    has_photo=has_photo,
                    has_buttons=has_buttons,
                    sent_at=datetime.now(),
                    groups_count=groups_count,
                )
                session.add(record)
                await session.flush()
                await session.refresh(record)
                session.expunge(record)
                return record

    @staticmethod
    @log_exc_with_try_except()
    async def get_last_broadcasts(limit: int = 20) -> list[BroadcastModel]:
        async with async_session() as session:
            result = await session.execute(
                select(BroadcastModel)
                .order_by(desc(BroadcastModel.sent_at))
                .limit(limit)
            )
            return result.scalars().all()
