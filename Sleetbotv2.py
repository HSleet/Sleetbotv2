import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text('klk wawawa!')


def help(update, context):
    update.message.reply_text('tamo en eso')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update {} caused error {}'.format(update, context.error))


def cat(update, context):
    update.message.reply


updater = Updater(token=BOT_TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_error_handler(error)
dp.add_handler(CommandHandler('cat', cat))

updater.start_polling()
updater.idle()

