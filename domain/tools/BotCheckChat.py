from aiogram.exceptions import TelegramMigrateToChat, TelegramForbiddenError

from data.repositories.ChatRepository import ChatRepository


async def check_bot_membership(bot, chat_id):
    chats = ChatRepository().all_chats()

    for chat in chats:
        results = ""

        try:
            await bot.get_chat_member(chat_id=chat['group_id'], user_id=bot.id)

            if chat['link'] is None:
                link = await bot.get_chat(chat['group_id'])
                if link.invite_link is not None and ChatRepository().update_chat_link(chat['group_id'], link.invite_link):
                    results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nОновлено лінку на групу\n\nВиправлено ✅"
                else:
                    results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nНе вийшло оновити лінку на групу (скоріше за все бот не доданий як адмін)\n\nНе виправлено ❌"
        except TelegramForbiddenError as e:
            if e.message.__contains__("bot was kicked from the group chat"):
                results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nБот був кікнутий з групи (Групу видалено з бази)\n\nВиправлено ✅"
            else:
                results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\n{e.message}\n\n Не виправлено ❌"
        except TelegramMigrateToChat as e:
            updated = ChatRepository().update_group_id(old_group_id=chat['group_id'], new_group_id=e.migrate_to_chat_id)
            if updated:
                print(f"check_bot_membership: group was updated old({chat['group_id']}), new({e.migrate_to_chat_id})")
                results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nГрупа змінила статус на супергрупу, змінено id\n\nВиправлено ✅"
            else:
                if ChatRepository().get_chat(e.migrate_to_chat_id):
                    if ChatRepository().remove_chat(chat['group_id']):
                        print(
                            f"check_bot_membership: group was updated old({chat['group_id']}), new({e.migrate_to_chat_id}), old removed")
                        results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nГрупа змінила статус на супер групу та була повторно додана до бази, тому стару видалено\n\nВиправлено ✅"
                    else:
                        print(
                            f"check_bot_membership: group was NOT updated old({chat['group_id']}), new({e.migrate_to_chat_id}), old not removed")
                        results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nСталася помилка(<b>group was NOT updated, old not removed</b>): {e}\n\nНе виправлено ❌"
                else:
                    print(
                        f"check_bot_membership: group was NOT updated old({chat['group_id']}), new({e.migrate_to_chat_id})")
                    results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nСталася помилка(<b>group was NOT updated</b>): {e}\n\nНе виправлено ❌"
        except Exception as e:
            print(f"check_bot_membership: no type error {e} ({chat['group_id']})")
            if ChatRepository().remove_chat(chat['group_id']):
                print(
                    f"check_bot_membership: group was deleted({chat['group_id']})")
                results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nПомилка: {e}\nГрупу видалено\n\nВиправлено ✅"
            else:
                print(
                    f"check_bot_membership: group was NOT deleted({chat['group_id']})")
                results += f"{chat['group_id']} | {chat['title']}\n{chat['link']}\n\nСталася помилка: {e}\nГрупу НЕ видалено\n\nНе виправлено ❌"
        if results:
            await bot.send_message(chat_id=chat_id, text=results)
