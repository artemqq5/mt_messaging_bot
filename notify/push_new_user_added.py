from repository.user_rep import UserRep


async def push_new_user_added(bot, message):
    admins_with_all_access = UserRep().get_admins_all_access()

    for admin in admins_with_all_access:
        try:
            await bot.send_message(chat_id=admin['telegram_id'], text=message)
        except Exception as e:
            print(f"push_new_user_added(): {e}")
