import os
from telegram.ext import *
from dotenv import load_dotenv

from src.controllers.Callback import Callback
from src.controllers.Replier import Replier

load_dotenv()
print('Starting...')

updater = Updater(os.getenv('TOKEN'))

# Set up the handlers for each type of message
replier = Replier()
updater.dispatcher.add_handler(MessageHandler(Filters.command, replier.handle_command))
updater.dispatcher.add_handler(MessageHandler(Filters.text, replier.handle_text))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, replier.handle_image))
updater.dispatcher.add_handler(MessageHandler(Filters.voice, replier.handle_voice))
updater.dispatcher.add_handler(MessageHandler(Filters.sticker, replier.handle_sticker))

# Set up the handler for callbacks
callback = Callback()
updater.dispatcher.add_handler(CallbackQueryHandler(callback.handle))

updater.start_polling()
print('Started!')

updater.idle()
