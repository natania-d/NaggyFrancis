import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import BaseFilter
from random import *
import re
import datetime

TOKEN = '424538023:AAG_WU0hiDPABPFKnm94UiatzjUFOuA6CP0'


bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
scolding_phrases = ["Mind your language, ", "Don't be rude, ", "Watch your mouth, ", "No vulgarities! Be a Francis, ", "Cool kids don't swear, ", "Mind your FUCKING manners, ", "Francis say cannot swear, ", "EH don't vulgar ah, "]
scolding_emojis = ["🙄", "😤", "🤐", "😑", "😲", "🖕🏻", "😨", "😡"]
vulgarity_list = ['fuck', 'fug', 'wtf', 'how', 'frick', 'freak', 'ass', 'ccb', 'knn', 'bitch', 'bij', 'screw', 'kanina', 'diu']
vulgarity_list_custom = []
today = datetime.date.today()
finals_date = datetime.date(2018, 4, 28)
finals_reminder = "Finals in " + str(finals_date - today).split(",")[0] + "! 😱"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class FilterVulgarities(BaseFilter):
    def filter(self, message):
    	compiled_lst = vulgarity_list + vulgarity_list_custom
    	return re.compile('|'.join(compiled_lst),re.IGNORECASE).search(message.text)

filter_vulgar = FilterVulgarities()


# Functions
def start(bot, update):
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=update.message.chat_id, text="Hi there! I am a copy cat, but I hate vulgarities! 😘")

def echo(bot, update):
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	rand = random()
	# A 10% chance to give finals reminder
	if rand <= 0.1:
		bot.send_message(chat_id=update.message.chat_id, text=finals_reminder)
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
	#bot.kick_chat_member(chat_id=chat_id, user_id=update.message.from_user.id)

def show_banned(bot, update):
	chat_id = update.message.chat_id
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	output = "" 
	for word in vulgarity_list:
		output += ("  •  " + word + "\n")
	for word in vulgarity_list_custom:
		output += ("  •  " + word + "\n")	
	bot.send_message(chat_id=chat_id, text="<b>Here is the list of banned words:</b>\n" + output, parse_mode=telegram.ParseMode.HTML)

def add_banned(bot, update, args):
	chat_id = update.message.chat_id
	if args:
		new_word = args[0]
	else:
		bot.send_message(chat_id=chat_id, text="No input, try again.")
		return 
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	if (new_word not in vulgarity_list_custom) and (new_word not in vulgarity_list):
		vulgarity_list_custom.append(new_word)
		bot.send_message(chat_id=chat_id, text="Vulgarity added! 😋")
	else:
		bot.send_message(chat_id=chat_id, text="Vulgarity already exists! 😒")

def remove_banned(bot, update, args):
	chat_id = update.message.chat_id
	if args:
		rm_word = args[0]
	else:
		bot.send_message(chat_id=chat_id, text="No input, try again.")
		return 		
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	if rm_word in vulgarity_list_custom:
		vulgarity_list_custom.remove(rm_word)
		bot.send_message(chat_id=chat_id, text=rm_word + " removed.")
	elif rm_word in vulgarity_list:
		bot.send_message(chat_id=chat_id, text="Default vulgarities cannot be removed! 😤")
	else:	
		bot.send_message(chat_id=chat_id, text="Vulgarity does not exist!")

def joke(bot, update):
	chat_id = update.message.chat_id
	sender_name = str(update.message.from_user.first_name)
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=chat_id, text="Here's a joke: " + sender_name)


def unknown(bot, update):
	chat_id = update.message.chat_id
	bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	update.message.reply_text("I'm sorry I'm afraid I can't do that.")


# Handlers
start_handler = CommandHandler('start', start)
vulgarities_handler = MessageHandler(filter_vulgar, vulgarities)
banned_handler = CommandHandler('banned', show_banned)
add_handler = CommandHandler('add', add_banned, pass_args=True)
remove_handler = CommandHandler('remove', remove_banned, pass_args=True)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)
joke_handler = CommandHandler('joke', joke)
unknown_handler = MessageHandler(Filters.command, unknown)

# Dispatching: As soon as you add new handlers to dispatcher, they are in effect.
dispatcher.add_handler(start_handler)
dispatcher.add_handler(remove_handler)
dispatcher.add_handler(banned_handler)
dispatcher.add_handler(vulgarities_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(joke_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
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
