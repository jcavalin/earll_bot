import sqlite3

# Helper for database
class Db:
    DATABASE = 'earll.db'

    def __init__(self):
        self.connection = sqlite3.connect(self.DATABASE)
        self.connection.row_factory = self.dict_factory
        self.create_tables()

    # Get a user from database
    def get_user(self, user, create_user=True, language='en'):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, language, voice FROM user_settings WHERE id = ?", (user,))
        result = cursor.fetchone()

        # If user doesn't exists, create
        if create_user and not result:
            self.create_user(user, language=language)
            result = self.get_user(user, create_user=False)

        return result

    # Create a user in database
    def create_user(self, user, language='en'):
        self.connection.execute("INSERT INTO user_settings (id, language) VALUES (?, ?);", (user, language))
        self.connection.commit()

    # Set the language for the user
    def set_language(self, user, language):
        self.connection.execute(
            "UPDATE user_settings SET language = ? WHERE id = ?;",
            (language, user)
        )
        self.connection.commit()

    # Set the voice for the user
    def set_voice(self, user, voice):
        self.connection.execute(
            "UPDATE user_settings SET voice = ? WHERE id = ?;",
            (voice, user)
        )
        self.connection.commit()

    # Initializes the database with tables
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

    # Factory to get data from database as a dictionary
    @staticmethod
    def dict_factory(cursor, row):
        result = {}
        for idx, col in enumerate(cursor.description):
            result[col[0]] = row[idx]

        return result
