from src.utils.Db import Db
from src.utils.Locale import Locale


# Represents the context of the application
class App:
    user = None
    db = None

    # Start application by the user
    @staticmethod
    def start(user):
        App.db = Db()
        App.user = App.db.get_user(user.id)
        Locale().load(App.user['language'])
