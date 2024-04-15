import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ChatMemberUpdated

import domain.routers.admin.chat.main_chat
from data.repositories.ChatRepository import ChatRepository
from domain.routers.admin.group import main_group
from private_cfg import BOT_TOKEN

# from notify.message_spam import spam_all_groups


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.my_chat_member()
async def chat_member_updated_handler(update: ChatMemberUpdated):
    if update.old_chat_member.status != 'member' and update.new_chat_member.status == 'member':
        ChatRepository().add_chat(group_id=update.chat.id, title=update.chat.title, datetime=datetime.now())


# @dp.message_handler(commands=['check_chats'], state='*')
# async def send_messeging_to_all(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is not None:
#         await state.reset_state()
#
#     if message.chat.type in [types.ChatType.PRIVATE, ]:
#         admin = UserRep()._is_admin(message.chat.id)
#         if admin is not None and admin['role'] == TypeOfAdmins.ADMIN.value:
#             await check_bot_membership(bot, message.chat.id)
#         else:
#             await message.answer("Відмовлено в доступі", reply_markup=ReplyKeyboardRemove())
#
#
# @dp.message_handler(commands=['messaging'], state='*')
# async def send_messeging_to_all(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is not None:
#         await state.reset_state()
#
#     if message.chat.type in [types.ChatType.PRIVATE, ]:
#         admin = UserRep()._is_admin(message.chat.id)
#         if admin is not None:
#             await StateMessage.category.set()
#             await message.answer("Оберіть тип чату для відправки: ", reply_markup=chat_type_category(admin))
#         else:
#             await message.answer("Відмовлено в доступі", reply_markup=ReplyKeyboardRemove())
#
#
# register_message_send_handler(dp)
#
#
# @dp.message_handler(lambda m: m.chat.type in [types.ChatType.GROUP, types.ChatType.SUPER_GROUP], state='*')
# async def all_message_handler(message: types.Message):
#     user_id = message['from']['id']
#
#     if not UserRep().is_user(user_id) and not UserRep().is_admin(user_id):
#
#         username = message['from']['username']
#         group_id = message['chat']['id']
#         time_added = message['date']
#         first_name = message['from']['first_name']
#         lang_code = message['from']['language_code']
#         chat_name = message['chat']['title']
#
#         link_group = await bot.get_chat(group_id)
#         link_group = link_group['invite_link']
#
#         if UserRep().add_user(user_id, username, group_id, time_added, first_name, lang_code, chat_name, link_group):
#             user_text = (f"👤 Новий користувач доданий до бази!\nusername: <b>@{username}</b> | {time_added}"
#                          f"\nID: <b>{user_id}</b>\ngroup: <b>{chat_name}</b>"
#                          f"\nlink: <b>{link_group}</b>")
#             # print(f"user @{username} was added")
#             await push_new_user_added(bot, user_text)


async def main():
    logging.basicConfig(level=logging.ERROR)
    default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=BOT_TOKEN, default=default_properties)

    dp.include_routers(
        domain.routers.admin.chat.main_chat.router,
        main_group.router
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


