from data.MyDataBase import MyDataBase
from data.other.accesses import TypeOfChats, has_value_enum


class ChatRepository(MyDataBase):
    def __init__(self):
        super().__init__()

    def add_chat(self, group_id, title, datetime):
        query = "INSERT INTO `chats` (`group_id`, `title`, `time`) VALUES (%s, %s, %s);"
        return self._insert(query, (group_id, title, datetime))

    def get_chat(self, group_id):
        query = "SELECT * FROM `chats` WHERE `group_id` = %s;"
        return self._select_one(query, (group_id,))

    def remove_chat(self, group_id):
        query = "DELETE FROM `chats` WHERE `group_id` = %s;"
        return self._delete(query, (group_id,))

    def update_chat_link(self, group_id, link):
        query = "UPDATE `chats` SET `link` = %s WHERE `group_id` = %s;"
        return self._update(query, (link, group_id))

    def all_chats(self):
        query = "SELECT * FROM `chats`;"
        return self._select(query)

    def chat_by_type(self, chat_type):
        if not has_value_enum(TypeOfChats, chat_type):
            return
        query = f"SELECT * FROM `chats` WHERE `{chat_type}` = '1';"
        return self._select(query)

    def unspecified_chats(self):
        query = (
            "SELECT * FROM `chats` WHERE  creo = 0 AND google = 0 AND fb = 0 AND console = 0 AND apps = 0 AND pp_web = 0 AND  pp_ads = 0 AND media = 0 AND agency_google = 0 AND agency_fb = 0;")
        return self._select(query)

    def update_chat_type(self, group_id, chat_type, available):
        if not has_value_enum(TypeOfChats, chat_type):
            return
        query = f"UPDATE `chats` SET `{chat_type}` = %s WHERE `group_id` = %s;"
        return self._update(query, (available, group_id))

    def update_group_id(self, old_group_id, new_group_id):
        query = "UPDATE `chats` SET `group_id` = %s WHERE `group_id` = %s;"
        return self._update(query, (new_group_id, old_group_id))
