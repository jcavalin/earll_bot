import os
from telegram.ext import *
from dotenv import load_dotenv
from services.Replier import Replier
from services.Commands import Commands

load_dotenv()
print('Starting...')

updater = Updater(os.getenv('TOKEN'))

commands = Commands()
replier = Replier(commands)

dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, replier.handle_text))
dispatcher.add_handler(MessageHandler(Filters.voice, replier.handle_voice))

updater.start_polling()
print('Started!')

updater.idle()
