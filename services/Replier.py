import traceback

from services.Command import Command
from services.Speech import Speech
from services.Vision import Vision


class Replier:

    def handle_text(self, update, context):
        print('Handling text')
        text = str(update.message.text)
        self.reply_from_text(text, update)

    def handle_sticker(self, update, context):
        print('Handling sticker')
        text = str(update.message.sticker.emoji)
        self.reply_from_text(text, update)

    def handle_voice(self, update, context):
        print('Handling voice')
        voice = update.message.voice

        speech = Speech()
        try:
            result = speech.to_text(voice)
            response = result.text
        except Exception as e:
            response = self.handle_error(e)
            speech.get_temp_file().delete_tmp_files()

        self.reply_text(update, response)

    def handle_image(self, update, context):
        print('Handling image')
        image = update.message.photo

        vision = Vision()
        try:
            result = vision.to_text(image[-1])
            self.reply_from_text(result.text, update, caption=result.text)
        except Exception as e:
            response = self.handle_error(e)
            self.reply_text(update, response)

    def handle_command(self, update, context):
        print(f'Handling command')
        text = str(update.message.text)

        try:
            command = Command()
            response = command.responses(text, self.replier(update))
        except Exception as e:
            response = self.handle_error(e)

        update.message.reply_text(response)

    def reply_from_text(self, text, update, caption: str = None):
        speech = Speech()

        try:
            response = speech.to_voice(text)

            with open(response['path'], 'rb') as file:
                update.message.reply_voice(
                    voice=file,
                    reply_to_message_id=update.message.message_id,
                    duration=response['duration'],
                    caption=caption
                )
        except Exception as e:
            response = self.handle_error(e)
            self.reply_text(update, response)

        speech.get_temp_file().delete_tmp_files()

    @staticmethod
    def replier(update):
        def reply_text(text):
            update.message.reply_text(text=text, reply_to_message_id=update.message.message_id)

        return reply_text

    @staticmethod
    def reply_text(update, text):
        update.message.reply_text(text=text, reply_to_message_id=update.message.message_id)

    @staticmethod
    def handle_error(e):
        print(f'Error: {e.__str__()} -> {traceback.format_exc()}')
        return "Error! 😔"
