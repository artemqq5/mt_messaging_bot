


# async def check_bot_membership(bot, chat_id):
#     chats = ChatRep()._all_chats()
#
#     results = ""
#
#     for chat in chats:
#         try:
#             await bot.get_chat_member(chat_id=chat['group_id'], user_id=bot.id)
#
#             if chat['link'] is None:
#                 link = await bot.get_chat(chat['group_id'])
#                 if link['invite_link'] is not None and ChatRep()._update_chat_link(chat['group_id'],
#                                                                                       link['invite_link']):
#                     results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nОновлено лінку на групу\n\n"
#                 else:
#                     results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\n Не вийшло оновити лінку на групу (скоріше за все бот не доданий як адмін)\n\n"
#         except ChatNotFound as e:
#             print(f"check_bot_membership: {chat['group_id']} | {chat['title']}\nГрупа не знайдена\n\n {e}")
#             results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nГрупа не знайдена\n\n"
#         except Exception as e:
#             if "The group has been migrated to a supergroup. New id" in str(e):
#                 new_group_id = str(e).split(" ")[-1].replace(".", "")
#                 print(f"check_bot_membership: {e}")
#                 updated = ChatRep().update_group_id(old_group_id=chat['group_id'], new_group_id=new_group_id)
#                 if updated:
#                     print(f"check_bot_membership: group was updated old({chat['group_id']}), new({new_group_id})")
#                     results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка(<b>group was updated</b>): {e}\n\n"
#                 else:
#                     if ChatRep()._get_chat(new_group_id):
#                         if ChatRep()._remove_chat(chat['group_id']):
#                             print(
#                                 f"check_bot_membership: group was updated old({chat['group_id']}), new({new_group_id}), old removed")
#                             results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка(<b>group was updated, old removed</b>): {e}\n\n"
#                         else:
#                             print(
#                                 f"check_bot_membership: group was NOT updated old({chat['group_id']}), new({new_group_id}), old not removed")
#                             results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка(<b>group was NOT updated, old not removed</b>): {e}\n\n"
#                     else:
#                         print(
#                             f"check_bot_membership: group was NOT updated old({chat['group_id']}), new({new_group_id})")
#                         results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка(<b>group was NOT updated</b>): {e}\n\n"
#
#             else:
#                 print(f"check_bot_membership: {chat['group_id']} | {chat['title']}\nСталася помилка\n\n {e}")
#                 results += f"{chat['group_id']} | {chat['title']} | {chat['link']}\nСталася помилка: <b>{e}</b>\n\n"
#
#     await bot.send_message(chat_id=chat_id, text=results)
