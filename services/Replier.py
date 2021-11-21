import traceback
from services.Speech import Speech


class Replier:

    def __init__(self, commands):
        self.commands = commands

    def handle_text(self, update, context):
        text = str(update.message.text)
        print(f'Handling text: {text}')

        try:
            # response = self.commands.responses(text, self.replier(update))
            speech = Speech()
            response = speech.to_voice(text)

            update.message.reply_voice(
                voice=open(response['path'], 'rb'),
                reply_to_message_id=update.message.message_id,
                duration=response['duration']
            )

            speech.get_temp_file().delete_tmp_files()
        except Exception as e:
            response = self.handle_error(e)
            update.message.reply_text(response, reply_to_message_id=update.message.message_id)

    def handle_voice(self, update, context):
        voice = update.message.voice
        print('Handling voice')

        try:
            speech = Speech()
            result = speech.to_text(voice)
            response = result.text
        except Exception as e:
            response = self.handle_error(e)

        update.message.reply_text(response, reply_to_message_id=update.message.message_id)

    @staticmethod
    def replier(update):
        def reply_message(text):
            update.message.reply_text(text=text)

        return reply_message

    @staticmethod
    def handle_error(e):
        print(f'Error: {e.__str__()} -> {traceback.format_exc()}')
        return "Error! 😔"
