from data.MyDataBase import MyDataBase


class AdminRepository(MyDataBase):

    def __init__(self):
        super().__init__()

    def is_admin(self, telegram_id):
        query = "SELECT * FROM `admins` WHERE `telegram_id` = %s;"
        return self._select_one(query, (telegram_id,))

    def get_admins(self):
        query = "SELECT * FROM `admins` WHERE `role` = 'ADMIN';"
        return self._select(query)
