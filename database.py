import pymysql

from config.cfg import DB_PASSWORD


class MyDataBase:
    def __init__(self):
        self.__connection = pymysql.connect(
            host="localhost",
            user="root",
            password=DB_PASSWORD,
            db="mt_messaging_db",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def _is_admin(self, telegram_id):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "SELECT * FROM `admins` WHERE `telegram_id` = %s;"
                    cursor.execute(_command, telegram_id)
                return cursor.fetchone()
        except Exception as e:
            print(f"_is_admin: {e}")
            return None

    def _add_chat(self, group_id, title):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "INSERT INTO `chats` (`group_id`, `title`) VALUES (%s, %s);"
                    cursor.execute(_command, (group_id, title))
                connection.commit()
                return True
        except Exception as e:
            print(f"_add_chat: {e}")
            return None

    def _all_chats(self):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "SELECT * FROM `chats`;"
                    cursor.execute(_command)
                return cursor.fetchall()
        except Exception as e:
            print(f"_all_chats: {e}")
            return None

    def _chat_by_type(self, chat_type):  # type args only from dict types
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = f"SELECT * FROM `chats` WHERE `{chat_type}` = '1';"
                    cursor.execute(_command)
                return cursor.fetchall()
        except Exception as e:
            print(f"chat_by_type: {e}")
            return None

    def _update_chat_creo(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `creo` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_creo: {e}")
            return None

    def _update_chat_google(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `google` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_google: {e}")
            return None

    def _update_chat_fb(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `fb` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_fb: {e}")
            return None

    def _update_chat_console(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `console` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_console: {e}")
            return None

    def _update_chat_pp_web(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `pp_web` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_pp_web: {e}")
            return None

    def _update_chat_pp_ads(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `pp_ads` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_pp_ads: {e}")
            return None

    def _update_chat_agency(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `pp_ads` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_agency: {e}")
            return None

    def _update_chat_apps(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `pp_ads` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_apps: {e}")
            return None

    def _update_chat_media(self, group_id, available):
        try:
            with self.__connection as connection:
                with connection.cursor() as cursor:
                    _command = "UPDATE `chats` SET `media` = %s WHERE `group_id` = %s;"
                    cursor.execute(_command, (available, group_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"_update_chat_media: {e}")
            return None


