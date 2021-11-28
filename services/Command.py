from services.Locale import Locale


class Command:
    def __init__(self):
        self.origin = None
        self.state = None

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

    @staticmethod
    def set_language(language=None):
        if language not in Locale.supported_languages:
            return Locale.get('supported_languages') + ', '.join(Locale.supported_languages)

        Locale.load(language)
        return Locale.get('done')

    @staticmethod
    def set_voice(voice=None):
        return Locale.get('done')
