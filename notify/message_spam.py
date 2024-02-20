from aiogram.types import ReplyKeyboardRemove

from database import MyDataBase
from repository.chat_rep import ChatRep


async def spam_all_groups(data, message, chat_type=None):
    try:
        chats = MyDataBase()._all_chats() if chat_type is None else MyDataBase()._chat_by_type(chat_type)
        counter = 0
        for chat in chats:
            try:
                await send_message(data, message, chat['group_id'])
                counter += 1
            except Exception as e:
                if "The group has been migrated to a supergroup. New id" in str(e):
                    new_group_id = str(e).split(" ")[-1].replace(".", "")
                    print(f"spam_group: {e}")
                    updated = ChatRep().update_group_id(old_group_id=chat['group_id'], new_group_id=new_group_id)
                    if updated:
                        print(f"group was updated and send again old({chat['group_id']}), new({new_group_id})")
                        try:
                            await send_message(data, message, new_group_id)
                            counter += 1
                        except Exception as e:
                            print(f"spam_group_repeat: {e}")
                    else:
                        print(f"group was NOT updated and send again old({chat['group_id']}), new({new_group_id})")
                else:
                    print(f"spam_group: {e}")
        await message.answer(
            "Сповіщення отримали {0} груп з {1}".format(counter, len(chats)),
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        print(f"spam_all_groups: {e}")


async def send_message(data, message, group_id):
    if data.get('photo', None) is not None:
        await message.bot.send_photo(chat_id=group_id, photo=data['photo'], caption=data['message'])
    elif data.get('video', None) is not None:
        await message.bot.send_video(chat_id=group_id, video=data['video'], caption=data['message'])
    elif data.get('gif', None) is not None:
        await message.bot.send_document(chat_id=group_id, document=data['gif'], caption=data['message'])
    else:
        await message.bot.send_message(chat_id=group_id, text=data['message'])
