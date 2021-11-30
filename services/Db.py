import sqlite3


class Db:
    def __init__(self):
        self.connection = sqlite3.connect('earll.db')
        self.connection.row_factory = self.dict_factory

    def get_user(self, user, create_user=True):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, language, voice FROM user_settings WHERE id = ?", (user,))
        result = cursor.fetchone()

        if create_user and not result:
            self.create_user(user)
            result = self.get_user(user, create_user=False)

        return result

    def create_user(self, user):
        self.connection.execute("INSERT INTO user_settings (id) VALUES (?);", (user,))
        self.connection.commit()

    def set_language(self, user, language):
        self.connection.execute(
            "UPDATE user_settings SET language = ? WHERE id = ?;",
            (language, user)
        )
        self.connection.commit()

    def set_voice(self, user, voice):
        self.connection.execute(
            "UPDATE user_settings SET voice = ? WHERE id = ?;",
            (voice, user)
        )
        self.connection.commit()

    @staticmethod
    def dict_factory(cursor, row):
        result = {}
        for idx, col in enumerate(cursor.description):
            result[col[0]] = row[idx]

        return result
