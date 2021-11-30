import traceback
from abc import ABC

from src.utils.App import App
from src.utils.Locale import Locale


class AbsController(ABC):
    app = None

    def app_start(self, user):
        App.start(user)
        self.app = App

    @staticmethod
    def handle_error(e):
        print(f'Error: {e.__str__()} -> {traceback.format_exc()}')
        return Locale.get('error')
