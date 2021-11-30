from src.utils.Db import Db
from src.utils.Locale import Locale


class App:
    user = None
    db = None

    @staticmethod
    def start(user):
        App.db = Db()
        App.user = App.db.get_user(user.id, language=user.language_code)
        Locale().load(App.user['language'])
