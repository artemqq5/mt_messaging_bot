import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ChatMemberUpdated

import domain.routers.admin.chat.main_chat
from private_cfg import BOT_TOKEN
from data.repositories.ChatRepository import ChatRepository
from domain.routers.admin.group import main_group
from domain.routers.user import main_

# from tools.message_spam import spam_all_groups


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# AUTOMATIC ADD CHAT TO DB
# @dp.my_chat_member()
# async def chat_member_updated_handler(update: ChatMemberUpdated):
#     if update.old_chat_member.status != 'member' and update.new_chat_member.status == 'member':
#         ChatRepository().add_chat(group_id=update.chat.id, title=update.chat.title, datetime=datetime.now())


async def main():
    logging.basicConfig(level=logging.ERROR)
    default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=BOT_TOKEN, default=default_properties)

    dp.include_routers(
        domain.routers.admin.chat.main_chat.router,
        main_group.router,
        main_.router
    )

    try:
        # start bot
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        print(f"start bot: {e}")
        return


if __name__ == '__main__':
    asyncio.run(main())


