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
            InlineKeyboardButton("Language", callback_data='set_language_options'),
            InlineKeyboardButton("Voice", callback_data='set_voice_options')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_reply_text = 'Here are your current settings:\n' \
                             + f"\tLanguage: {self.user['language']}\n" \
                             + f"\tVoice: {self.user['voice']}\n" \
                             + '\n' \
                             + 'What would you like to set up?'

        self.replier(message_reply_text, reply_markup)

    @staticmethod
    def language_options(replier):
        keyboard = [[
            InlineKeyboardButton("English", callback_data='set_language_en'),
            InlineKeyboardButton("Português", callback_data='set_language_pt')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = 'What language would you like to change to?'

        replier(text, reply_markup)

    @staticmethod
    def voice_options(replier):
        keyboard = [[
            InlineKeyboardButton("Male", callback_data='set_voice_male'),
            InlineKeyboardButton("Female", callback_data='set_voice_female')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = 'What voice would you like to change to?'

        replier(text, reply_markup)
