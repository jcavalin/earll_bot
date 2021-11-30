from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.Locale import Locale


class Command:
    replier = None

    def __init__(self, user, db):
        self.user = user
        self.db = db

    def responses(self, text, replier):
        self.replier = replier
        input_text = str(text).lower().split(' ')
        command = input_text[0]
        arg = ''

        if 0 <= 1 < len(input_text):
            arg = input_text[1]

        switch = {
            '/language': self.set_language,
            '/voice': self.set_voice,
            '/settings': self.settings
        }

        return switch.get(command, self.greetings)(arg)

    @staticmethod
    def greetings(arg=None):
        return Locale.get('hi')

    def set_language(self, language):
        if language not in Locale.supported_languages:
            return Locale.get('must_choose') + ', '.join(Locale.supported_languages)

        self.db.set_language(self.user['id'], language)
        Locale.load(language)
        return Locale.get('done')

    def set_voice(self, voice):
        voices = ['male', 'female']

        if voice not in voices:
            return Locale.get('must_choose') + ', '.join(voices)

        self.db.set_voice(self.user['id'], voice)
        return Locale.get('done')

    def settings(self, args=None):
        keyboard = [[
            InlineKeyboardButton(Locale.get('language'), callback_data='set_language_options'),
            InlineKeyboardButton(Locale.get('voice'), callback_data='set_voice_options')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_reply_text = Locale.get('current_settings') + ':\n' \
                             + f"\t{Locale.get('language')}: {self.user['language']}\n" \
                             + f"\t{Locale.get('voice')}: {self.user['voice']}\n" \
                             + '\n' \
                             + Locale.get('setup_question')

        self.replier(message_reply_text, reply_markup)

    @staticmethod
    def language_options(replier):
        keyboard = [[
            InlineKeyboardButton("English", callback_data='set_language_en'),
            InlineKeyboardButton("Português", callback_data='set_language_pt')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = Locale.get('language_question')

        replier(text, reply_markup)

    @staticmethod
    def voice_options(replier):
        keyboard = [[
            InlineKeyboardButton(Locale.get('male'), callback_data='set_voice_male'),
            InlineKeyboardButton(Locale.get('female'), callback_data='set_voice_female')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = Locale.get('voice_question')

        replier(text, reply_markup)
