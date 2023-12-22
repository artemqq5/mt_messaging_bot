import pymysql

from cfg import DB_PASSWORD


class MyDataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password=DB_PASSWORD,
            db="mt_messaging_db",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def is_admin(self, telegram_id):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = "SELECT * FROM `admins` WHERE `telegram_id` = %s;"
                    cursor.execute(_command, telegram_id)
                return cursor.fetchone()
        except Exception as e:
            print(f"is_admin: {e}")
            return None

    def add_chat(self, group_id, title):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = "INSERT INTO `chats` (`group_id`, `title`) VALUES (%s, %s);"
                    cursor.execute(_command, (group_id, title))
                connection.commit()
                return True
        except Exception as e:
            print(f"add_chat: {e}")
            return None

    def all_chats(self):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = "SELECT * FROM `chats`;"
                    cursor.execute(_command)
                return cursor.fetchall()
        except Exception as e:
            print(f"is_admin: {e}")
            return None

