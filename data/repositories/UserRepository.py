from data.MyDataBase import MyDataBase


class Userrepisitory(MyDataBase):

    def __init__(self):
        super().__init__()

    def is_user(self, user_id):
        query = "SELECT * FROM `users` WHERE `user_id` = %s;"
        return self._select_one(query, (user_id,))

    def add_user(self, user_id, username, group_id, time, first_name, lang_code, chat_name, link_group):
        query = "INSERT INTO `users` (`user_id`, `username`, `group_id`, `time`, `first_name`, `language_code`, `title_gruop`, `link_group`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
        return self._insert(query, (user_id, username, group_id, time, first_name, lang_code, chat_name, link_group))
