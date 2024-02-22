from aiogram.utils.exceptions import ChatNotFound

from database import MyDataBase
from repository.chat_rep import ChatRep


async def check_bot_membership(bot, chat_id):
    chats = MyDataBase()._all_chats()

    results = ""

    for chat in chats:
        try:
            await bot.get_chat_member(chat_id=chat['group_id'], user_id=bot.id)

            if chat['link'] is None:
                link = await bot.get_chat(chat['group_id'])
                if link is not None:
                    if MyDataBase()._update_chat_link(chat['group_id'], link['invite_link']):
                        results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nОновлено лінку на групу\n\n"
        except ChatNotFound as e:
            print(f"check_bot_membership: {chat['group_id']} | {chat['title']}\nГрупа не знайдена\n\n {e}")
            results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nГрупа не знайдена\n\n"
        except Exception as e:
            if "The group has been migrated to a supergroup. New id" in str(e):
                new_group_id = str(e).split(" ")[-1].replace(".", "")
                print(f"check_bot_membership: {e}")
                updated = ChatRep().update_group_id(old_group_id=chat['group_id'], new_group_id=new_group_id)
                if updated:
                    print(f"check_bot_membership: group was updated and send again old({chat['group_id']}), new({new_group_id})")
                    results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка(group was updated): {e}\n\n"
                else:
                    print(f"check_bot_membership: group was NOT updated and send again old({chat['group_id']}), new({new_group_id})")
                    results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка(group was NOT updated): {e}\n\n"
            else:
                print(f"check_bot_membership: {chat['group_id']} | {chat['title']}\nСталася помилка\n\n {e}")
                results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка: {e}\n\n"

    await bot.send_message(chat_id=chat_id, text=results)

