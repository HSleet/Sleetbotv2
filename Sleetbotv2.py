import os
import logging
import sqlite3
import cat_gen

from uuid import uuid4
from telegram import InlineQueryResultAudio
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")


def db_query(search_keywords):
    with sqlite3.connect('alofoke.db') as conn:
        kw_list = search_keywords.split()
        query_match = [f'%{keyword}%' for keyword in kw_list]
        query_match = ' '.join(query_match)
        c = conn.cursor()
        c.execute(f"SELECT songs.artist, songs.song_name, songs.file_url FROM songs WHERE song_name LIKE '{query_match}' OR artist LIKE '{query_match}'")
        songs = c.fetchmany(25)
    return songs


def inlinequery(update, context):
    query = update.inline_query.query
    query_result = db_query(query)
    results = [
        InlineQueryResultAudio(
            id=uuid4(),
            title=song[1],
            audio_url=song[-1],
            performer=song[0],)
        for song in query_result
    ]
    update.inline_query.answer(results)


def start(update, context):
    update.message.reply_text('klk wawawa!')


def help(update, context):
    update.message.reply_text('')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update {} caused error {}'.format(update, context.error))


def cat(update, context):
    kitten = cat_gen.get_cat()
    update.message.reply_photo(kitten, quote=True)


def reverse(update, context):
    text = context.args
    text = ' '.join(text)
    reverse_text = text[::-1]
    update.message.reply_text(reverse_text)


updater = Updater(token=BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('reverse', reverse))
dp.add_handler(CommandHandler('cat', cat))
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(InlineQueryHandler(inlinequery))
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_error_handler(error)


updater.start_polling()
updater.idle()

