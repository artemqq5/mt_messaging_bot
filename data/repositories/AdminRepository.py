from data.MyDataBase import MyDataBase


class AdminRepository(MyDataBase):

    def __init__(self):
        super().__init__()

    def is_admin(self, telegram_id):
        query = "SELECT * FROM `admins` WHERE `telegram_id` = %s;"
        return self._select_one(query, (telegram_id,))

    # def get_admin_access(self):
    #     try:
    #         with self.__connection as connection:
    #             with connection.cursor() as cursor:
    #                 _command = "SELECT * FROM `admins` WHERE `role` = %s;"
    #                 cursor.execute(_command, TypeOfAdmins.ADMIN.value)
    #             return cursor.fetchall()
    #     except Exception as e:
    #         print(f"_get_admins_all_access: {e}")
    #         return None

