import os
import logging
from bot_functions import text_functions, urban_dict, spotify_parser
from bot_functions.spotify_parser import Track
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Bot


PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

debug = os.getenv("DEBUG")
if debug == "True":
    BOT_TOKEN = os.getenv("TEST_BOT_TOKEN")
else:
    BOT_TOKEN = os.getenv("BOT_TOKEN")


def error(update, context):
    logger.warning('Update {} caused error: {}'.format(update, context.error))


def reverse(update, context):
    text = context.args
    text = ' '.join(text)
    reverse_text = text_functions.reverse(text)
    update.message.reply_text(reverse_text)


def urban_dictionary(update, context):
    text = ' '.join(context.args)
    definition = urban_dict.get_definition(text)
    markdown_definition, markdown_example = definition.get_markdown_text()
    reply_message = f"*{definition.word}*: \n\n{markdown_definition}\n\nExample:\n\n{markdown_example}\n\nAuthor:" \
                    f"\t`{definition.author}`"
    update.message.reply_text(text=reply_message,
                              parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True,)


def mocking_text(update, context):
    text = context.args
    text = ' '.join(text)
    mock_text = text_functions.mock_text(text)
    update.message.reply_text(mock_text)


def spotify_search(update, context):
    text = " ".join(context.args)
    top_5_songs = spotify_parser.search_query(search_parameter=text)
    button_list = [
        [InlineKeyboardButton(f'{song["song"]["name"]} - {song["artists"]}',
                              callback_data=song["song"]["song_id"])] for song in top_5_songs
    ]
    keyboard = InlineKeyboardMarkup(button_list)
    update.message.reply_text("which song is it?", reply_markup=keyboard)


def spotify_button(update, context):
    query = update.callback_query
    query.answer()
    track = Track(track_id=query.data)
    md_song = f"[{track.name}]({track.url})\n[{track.artist.artist_name}]({track.artist.artist_url})"
    query.message.delete()
    button_list = [[InlineKeyboardButton("Open in spotify", url=track.url)]]
    keyboard = InlineKeyboardMarkup(button_list)
    bot.send_message(chat_id=query.message.chat_id,
                     text=md_song,
                     parse_mode=ParseMode.MARKDOWN,
                     disable_web_page_preview=True,
                     reply_markup=keyboard)
    print(track.preview)
    bot.send_audio(chat_id=query.message.chat_id,
                   audio=track.preview)


updater = Updater(token=BOT_TOKEN, use_context=True)

updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=BOT_TOKEN)
updater.start_webhook("https://sleetbot.herokuapp.com/"+BOT_TOKEN)
bot = Bot(token=BOT_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('reverse', reverse))
dp.add_handler(CommandHandler('mock', mocking_text))
dp.add_handler(CommandHandler('spotify', spotify_search))
dp.add_handler(CallbackQueryHandler(spotify_button, pattern=r'^[a-zA-Z0-9]{22}$'))

dp.add_handler(CommandHandler('ud', urban_dictionary))

# dp.add_handler(CommandHandler('cat', cat))
# dp.add_handler(CommandHandler("start", start))
# dp.add_handler(CommandHandler("help", help_func))
# dp.add_handler(InlineQueryHandler(inlinequery))
# dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_error_handler(error)

updater.start_polling()
updater.idle()
