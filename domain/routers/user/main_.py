from datetime import datetime

from aiogram import Router, F, types, Bot

from data.repositories.UserRepository import UserRepository
from domain.middlewares.IsGroupUser import IsGroupUser
from domain.tools.MessageSpamTool import push_new_user_added

router = Router()

router.message.middleware(IsGroupUser())


@router.message()
async def all_message_handler(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username
    group_id = message.chat.id
    time_added = datetime.now()
    first_name = message.from_user.first_name
    lang_code = message.from_user.language_code
    chat_name = message.chat.title

    link_group = await bot.get_chat(group_id)
    link_group = link_group.invite_link if link_group else None

    if UserRepository().add_user(user_id, username, group_id, time_added, first_name, lang_code, chat_name, link_group):
        user_text = (f"👤 Новий користувач доданий до бази!\nusername: <b>@{username}</b> | {time_added}"
                     f"\nID: <b>{user_id}</b>\ngroup: <b>{chat_name}</b>"
                     f"\nlink: <b>{link_group}</b>")
        # print(f"user @{username} was added")
        await push_new_user_added(bot, user_text)
