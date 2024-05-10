import pymysql

from config.private_cfg import DB_PASSWORD


class MyDataBase:
    def __init__(self):
        self.__connection = pymysql.connect(
            host="localhost",
            user="root",
            password=DB_PASSWORD,
            db="mt_messaging_db",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def _insert(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_insert: {e}")

    def _update(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_update: {e}")

    def _delete(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    return cursor.execute(query, args)
        except Exception as e:
            print(f"_delete: {e}")

    def _select_one(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    return cursor.fetchone()
        except Exception as e:
            print(f"_select_one: {e}")

    def _select(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    return cursor.fetchall()
        except Exception as e:
            print(f"_select_all: {e}")
