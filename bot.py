import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import BaseFilter
from random import randint
import re


TOKEN = '424538023:AAG_WU0hiDPABPFKnm94UiatzjUFOuA6CP0'

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
scolding_phrases = ["Mind your language, ", "Don't be rude, ", "Watch your mouth, ", "No vulgarities! Be a Francis, ", "Cool kids don't swear, ", "Mind your FUCKING manners, ", "Francis say cannot swear, ", "EH don't vulgar ah, "]
scolding_emojis = ["🙄", "😤", "🤐", "😑", "😲", "🖕🏻", "😨", "😡"]
vulgarity_list = ['fuck', 'fug', 'wtf', 'how', 'frick', 'freak']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class FilterVulgarities(BaseFilter):
    def filter(self, message):
        return re.compile('|'.join(vulgarity_list),re.IGNORECASE).search(message.text)


filter_vulgar = FilterVulgarities()


# Functions
def start(bot, update):
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=update.message.chat_id, text="Hi there! I am a copy cat, but I hate vulgarities! 😘")

def echo(bot, update):
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def vulgarities(bot, update):
	chat_id = update.message.chat_id
	sender_name = str(update.message.from_user.first_name)
	chosen = randint(0, len(scolding_phrases) - 1)
	bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=chat_id, text=scolding_phrases[chosen] + sender_name + "! " + scolding_emojis[chosen])


def inline_caps(bot, update):
	query = update.inline_query.query
	if not query:
		return
	results = list()
	results.append(
		InlineQueryResultArticle(
			id=query.upper(),
			title='Caps',
			input_message_content=InputTextMessageContent(query.upper())
		)
	)
	bot.answer_inline_query(update.inline_query.id, results)

def unknown(bot, update):
	chat_id = update.message.chat_id
	bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	update.message.reply_text("I'm sorry I'm afraid I can't do that.")
	button_list = [
    	InlineKeyboardButton("col1", callback_data="col1"),
    	InlineKeyboardButton("col2", callback_data="col2"),
    	InlineKeyboardButton("row 2", callback_data="row2")
	]
	reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
	bot.send_message(chat_id=chat_id, text="A two-column menu", reply_markup=reply_markup)

# Handlers
start_handler = CommandHandler('start', start)
vulgarities_handler = MessageHandler(filter_vulgar, vulgarities)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)
inline_caps_handler = InlineQueryHandler(inline_caps)
unknown_handler = MessageHandler(Filters.command, unknown)

# Dispatching: As soon as you add new handlers to dispatcher, they are in effect.
dispatcher.add_handler(start_handler)
dispatcher.add_handler(vulgarities_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(unknown_handler) # MUST be the last handler to be added

# Run the bot
updater.start_polling()


"""
bot.send_message(chat_id=update.message.chat_id, text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', parse_mode=telegram.ParseMode.HTML)

Custom keyboard code:
	custom_keyboard = [['top-left', 'top-right'], ['bottom-left', 'bottom-right']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	bot.send_message(chat_id=chat_id, text="Custom Keyboard Test", reply_markup=reply_markup)

"""
