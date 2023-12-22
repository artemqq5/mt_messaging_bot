from database import MyDataBase


async def spam_all_groups(data, message):
    try:
        chats = MyDataBase().all_chats()
        counter = 0
        for chat in chats:
            try:
                if data.get('photo', None) is not None:
                    await message.bot.send_photo(chat_id=chat['group_id'], photo=data['photo'], caption=data['message'])
                else:
                    await message.bot.send_message(chat_id=chat['group_id'], text=data['message'])

                counter += 1
            except Exception as e:
                print(f"spam_all_groups: {e}")
        await message.answer("Сповіщення отримали {0} груп з {1}".format(counter, len(chats)))
    except Exception as e:
        print(f"spam_all_groups: {e}")
