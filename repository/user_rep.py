from database import MyDataBase


class UserRep(MyDataBase):
    def is_admin(self, telegram_id):
        return self._is_admin(telegram_id)

    def is_user(self, user_id):
        return self._is_user(user_id)

    def add_user(self, user_id, username, group_id, time, first_name, lang_code, chat_name, link_group):
        return self._add_user(user_id, username, group_id, time, first_name, lang_code, chat_name, link_group)

    def get_admins_all_access(self):
        return self._get_admins_all_access()
