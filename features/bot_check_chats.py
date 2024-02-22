from aiogram.utils.exceptions import ChatNotFound

from database import MyDataBase


async def check_bot_membership(bot, chat_id):
    chats = MyDataBase()._all_chats()

    results = ""

    for chat in chats:
        try:
            member = await bot.get_chat_member(chat_id=chat['group_id'], user_id=bot.id)

            if chat['link'] is None:
                link = await bot.get_chat(chat['group_id'])
                if link is not None:
                    if MyDataBase()._update_chat_link(chat['group_id'], link['invite_link']):
                        results = f"{chat['group_id']} | {chat['title']} | {chat['link']}\nОновлено лінку на групу\n\n"
        except ChatNotFound as e:
            print(f"check_bot_membership: {chat['group_id']} | {chat['title']}\nГрупа не знайдена\n\n {e}")
            results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nГрупа не знайдена\n\n"
        except Exception as e:
            print(f"check_bot_membership: {chat['group_id']} | {chat['title']}\nСталася помилка\n\n {e}")
            results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка: {e}\n\n"

    await bot.send_message(chat_id=chat_id, text=results)

