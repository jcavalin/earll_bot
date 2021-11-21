import traceback

from services.SpeechToText import SpeechToText


class Replier:

    def __init__(self, commands):
        self.commands = commands

    def handle_text(self, update, context):
        text = str(update.message.text)
        print(f'Handling text: {text}')

        try:
            response = self.commands.responses(text, self.replier(update))
        except Exception as e:
            print(f'Error: {e.__str__()} -> {traceback.format_exc()}')
            response = "Error! 😔"

        update.message.reply_text(response)

    def handle_voice(self, update, context):
        voice = update.message.voice
        print(f'Handling voice')

        try:
            speech_to_text = SpeechToText()
            result = speech_to_text.recognize(voice)
            response = result.text
        except Exception as e:
            print(f'Error: {e.__str__()} -> {traceback.format_exc()}')
            response = "Error! 😔"

        update.message.reply_text(response)

    @staticmethod
    def replier(update):
        def reply_message(text):
            update.message.reply_text(text=text)

        return reply_message
