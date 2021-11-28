import os
from telegram.ext import *
from dotenv import load_dotenv
from services.Replier import Replier

load_dotenv()
print('Starting...')

updater = Updater(os.getenv('TOKEN'))
replier = Replier()

updater.dispatcher.add_handler(MessageHandler(Filters.command, replier.handle_command))
updater.dispatcher.add_handler(MessageHandler(Filters.text, replier.handle_text))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, replier.handle_image))
updater.dispatcher.add_handler(MessageHandler(Filters.voice, replier.handle_voice))
updater.dispatcher.add_handler(MessageHandler(Filters.sticker, replier.handle_sticker))

updater.start_polling()
print('Started!')

updater.idle()
