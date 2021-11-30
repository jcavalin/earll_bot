from src.controllers.AbsController import AbsController
from src.services.Command import Command
from src.services.Speech import Speech
from src.services.Vision import Vision


class Replier(AbsController):
    # Text message handler
    def handle_text(self, update, context):
        self.app_start(update.message.from_user)

        print('Handling text')
        text = str(update.message.text)
        self.reply_from_text(text, update)

    # Sticker message handler
    def handle_sticker(self, update, context):
        self.app_start(update.message.from_user)

        print('Handling sticker')
        text = str(update.message.sticker.emoji)
        self.reply_from_text(text, update)

    # Voice message handler
    def handle_voice(self, update, context):
        self.app_start(update.message.from_user)

        print('Handling voice')
        voice = update.message.voice

        speech = Speech(self.app.user['language'], self.app.user['voice'])
        try:
            result = speech.to_text(voice)
            response = result.text
        except Exception as e:
            response = self.handle_error(e)
            speech.get_temp_file().delete_tmp_files()

        self.reply_text(update, response)

    # Image message handler
    def handle_image(self, update, context):
        self.app_start(update.message.from_user)

        print('Handling image')
        image = update.message.photo

        vision = Vision()
        try:
            result = vision.to_text(image[-1], language=self.app.user['language'])
            self.reply_from_text(result.text, update, caption=result.text)
        except Exception as e:
            response = self.handle_error(e)
            self.reply_text(update, response)

    # Command message handler
    def handle_command(self, update, context):
        self.app_start(update.message.from_user)

        print(f'Handling command')
        text = str(update.message.text)

        try:
            command = Command(user=self.app.user, db=self.app.db)
            response = command.responses(text, self.replier(update))
        except Exception as e:
            response = self.handle_error(e)

        if response:
            update.message.reply_text(response)

    # Replies user with text and audio
    def reply_from_text(self, text, update, caption: str = None):
        speech = Speech(self.app.user['language'], self.app.user['voice'])

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

    # Replies user
    @staticmethod
    def replier(update):
        def reply_markup(text, markup):
            update.message.reply_text(text, reply_markup=markup)

        return reply_markup

    # Replies a text
    @staticmethod
    def reply_text(update, text):
        update.message.reply_text(text=text, reply_to_message_id=update.message.message_id)
