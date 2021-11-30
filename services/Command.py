from services.Locale import Locale


class Command:
    def __init__(self, user, db):
        self.user = user
        self.db = db

    def responses(self, text, reply):
        input_text = text.split(' ')
        command = str(input_text[0]).lower()
        arg = ''

        if 0 <= 1 < len(input_text):
            arg = input_text[1]

        switch = {
            '/language': self.set_language,
            '/voice': self.set_voice
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
