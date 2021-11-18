import traceback


class Replier:

    def __init__(self, commands):
        self.commands = commands

    def handle(self, update, context):
        text = str(update.message.text)

        print(f'Handling command: {text}')

        try:
            response = self.commands.responses(text, self.replier(update))
        except Exception as e:
            print(f'Error: {e.__str__()} -> {traceback.format_exc()}')
            response = "Error! 😔"

        update.message.reply_text(response)

    @staticmethod
    def replier(update):
        def reply_message(text):
            update.message.reply_text(text=text)

        return reply_message
