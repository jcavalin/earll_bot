import traceback

from src.services.Command import Command
from src.utils.Db import Db
from src.utils.Locale import Locale
from src.services.Speech import Speech
from src.services.Vision import Vision


class Replier:
    user = None
    db = None

    def set_user(self, user):
        self.db = Db()
        self.user = self.db.get_user(user.id, language=user.language_code)
        Locale().load(self.user['language'])

    def handle_text(self, update, context):
        self.set_user(update.message.from_user)

        print('Handling text')
        text = str(update.message.text)
        self.reply_from_text(text, update)

    def handle_sticker(self, update, context):
        self.set_user(update.message.from_user)

        print('Handling sticker')
        text = str(update.message.sticker.emoji)
        self.reply_from_text(text, update)

    def handle_voice(self, update, context):
        self.set_user(update.message.from_user)

        print('Handling voice')
        voice = update.message.voice

        speech = Speech(self.user['language'], self.user['voice'])
        try:
            result = speech.to_text(voice)
            response = result.text
        except Exception as e:
            response = self.handle_error(e)
            speech.get_temp_file().delete_tmp_files()

        self.reply_text(update, response)

    def handle_image(self, update, context):
        self.set_user(update.message.from_user)

        print('Handling image')
        image = update.message.photo

        vision = Vision()
        try:
            result = vision.to_text(image[-1], language=self.user['language'])
            self.reply_from_text(result.text, update, caption=result.text)
        except Exception as e:
            response = self.handle_error(e)
            self.reply_text(update, response)

    def handle_command(self, update, context):
        self.set_user(update.message.from_user)

        print(f'Handling command')
        text = str(update.message.text)

        try:
            command = Command(user=self.user, db=self.db)
            response = command.responses(text, self.replier(update))
        except Exception as e:
            response = self.handle_error(e)

        update.message.reply_text(response)

    def reply_from_text(self, text, update, caption: str = None):
        speech = Speech(self.user['language'], self.user['voice'])

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
        return Locale.get('error')
