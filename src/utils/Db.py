import sqlite3


class Db:
    DATABASE = 'earll.db'

    def __init__(self):
        self.connection = sqlite3.connect(self.DATABASE)
        self.connection.row_factory = self.dict_factory
        self.create_tables()

    def get_user(self, user, create_user=True, language='en'):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, language, voice FROM user_settings WHERE id = ?", (user,))
        result = cursor.fetchone()

        if create_user and not result:
            self.create_user(user, language=language)
            result = self.get_user(user, create_user=False)

        return result

    def create_user(self, user, language='en'):
        self.connection.execute("INSERT INTO user_settings (id, language) VALUES (?, ?);", (user, language))
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

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        if cursor.fetchone():
            return True

        cursor.execute("""
            CREATE TABLE user_settings (
                id integer not null primary key,
                voice varchar(100) not null default 'female',
                language varchar(100) not null default 'en'
            );
        """)

    @staticmethod
    def dict_factory(cursor, row):
        result = {}
        for idx, col in enumerate(cursor.description):
            result[col[0]] = row[idx]

        return result
