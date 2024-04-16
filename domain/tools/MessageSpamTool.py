from aiogram.exceptions import TelegramMigrateToChat
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.repositories.AdminRepository import AdminRepository
from data.repositories.ChatRepository import ChatRepository
from presentation.keyboard.admin_ import kb_main


async def spam_all_groups(data, message, chat_type=None):
    try:
        chats = ChatRepository().all_chats() if chat_type is None else ChatRepository().chat_by_type(chat_type)
        counter = 0
        for chat in chats:
            try:
                await send_message(data, message, chat['group_id'])
                counter += 1
            except TelegramMigrateToChat as e:
                updated = ChatRepository().update_group_id(old_group_id=chat['group_id'],
                                                           new_group_id=e.migrate_to_chat_id)
                if updated:
                    print(f"group was updated and send again old({chat['group_id']}), new({e.migrate_to_chat_id})")
                    try:
                        await send_message(data, message, e.migrate_to_chat_id)
                        counter += 1
                    except Exception as e:
                        print(f"spam_group_repeat: {e}")
                else:
                    print(f"group was NOT updated and send again old({chat['group_id']}), new({e.migrate_to_chat_id})")
            except Exception as e:
                print(f"check_bot_membership: no type error ({chat['group_id']}) {e}")
        await message.answer(
            "Сповіщення отримали {0} груп з {1}".format(counter, len(chats)),
            reply_markup=kb_main.as_markup()
        )
    except Exception as e:
        print(f"spam_all_groups: {e}")


async def send_message(data, message, group_id):
    if data.get('btn_text', None):
        kb = InlineKeyboardBuilder(
            markup=[[InlineKeyboardButton(text=data['btn_text'], url=data['btn_url'])]]).as_markup()
    else:
        kb = ReplyKeyboardRemove()

    if data.get('photo', None) is not None:
        await message.bot.send_photo(chat_id=group_id, photo=data['photo'], caption=data['message'], reply_markup=kb)
    elif data.get('video', None) is not None:
        await message.bot.send_video(chat_id=group_id, video=data['video'], caption=data['message'], reply_markup=kb)
    elif data.get('animation', None) is not None:
        await message.bot.send_animation(chat_id=group_id, animation=data['animation'], caption=data['message'], reply_markup=kb)
    else:
        await message.bot.send_message(chat_id=group_id, text=data['message'], reply_markup=kb)


async def push_new_user_added(bot, message):
    admins_with_all_access = AdminRepository().get_admins()

    for admin in admins_with_all_access:
        try:
            await bot.send_message(chat_id=admin['telegram_id'], text=message)
        except Exception as e:
            print(f"push_new_user_added(): {e}")
