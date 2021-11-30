from src.controllers.AbsController import AbsController
from src.services.Command import Command
from src.utils.Locale import Locale


class Callback(AbsController):
    def handle(self, update, context):
        self.app_start(update.callback_query.from_user)

        options = {
            'set_language_options': self.set_language_options,
            'set_voice_options': self.set_voice_options,
            'set_language_en': self.set_language_en,
            'set_language_pt': self.set_language_pt,
            'set_voice_male': self.set_voice_male,
            'set_voice_female': self.set_voice_female,
        }

        return options.get(update.callback_query.data)(update, context)

    def set_language_options(self, update, context):
        Command.language_options(self.replier(update, context))

    def set_voice_options(self, update, context):
        Command.voice_options(self.replier(update, context))

    def set_language_en(self, update, context):
        self.set_language(update, context, 'en')

    def set_language_pt(self, update, context):
        self.set_language(update, context, 'pt')

    def set_voice_male(self, update, context):
        self.set_voice(update, context, 'male')

    def set_voice_female(self, update, context):
        self.set_voice(update, context, 'female')

    def set_language(self, update, context, language):
        command = Command(user=self.app.user, db=self.app.db)
        command.set_language(language)
        replier = self.replier(update, context)
        replier(Locale.get('done'))

    def set_voice(self, update, context, voice):
        command = Command(user=self.app.user, db=self.app.db)
        command.set_voice(voice)
        replier = self.replier(update, context)
        replier(Locale.get('done'))

    @staticmethod
    def replier(update, context):
        def reply_markup(text, markup=None):
            context.bot.edit_message_text(
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,
                text=text,
                reply_markup=markup
            )

        return reply_markup
