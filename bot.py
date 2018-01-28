import telegram
from telegram.ext import Updater
from random_words import RandomWords
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import BaseFilter
from random import *
import re
import datetime
from lyrics import *


TOKEN = '424538023:AAG_WU0hiDPABPFKnm94UiatzjUFOuA6CP0'


bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
scolding_phrases = ["Mind your language, ", "Don't be rude, ", "Watch your mouth, ", "No vulgarities! Be a Francis, ", "Cool kids don't swear, ", "Mind your freaking manners, ", "Francis say cannot swear, ", "Eh don't vulgar ah, "]
scolding_emojis = ["🙄", "😤", "🤐", "😑", "😲", "🖕🏻", "😨", "😡"]
vulgarity_list = ['fuck', 'fug', 'wtf', 'frick', 'freak', 'asshole', 'ccb', 'knn', 'bitch', 'bij', 'screw', 'kanina', 'diu', 'smlj']
banned_list_custom = []
today = datetime.date.today()
finals_date = datetime.date(2018, 4, 28)
finals_reminder_text = "Guys, finals in " + str(finals_date - today).split(",")[0] + "! 😱"
song_holder = ""
date_last_added = datetime.date.today()
leaderboard = {}
non_vulgarities = {

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class FilterVulgarities(BaseFilter):
    def filter(self, message):	
    	compiled_lst = vulgarity_list + banned_list_custom
    	return re.compile('|'.join(compiled_lst),re.IGNORECASE).search(message.text)

class FilterSongs(BaseFilter):
	def filter(self, message):
		word_lst = message.text.lower().split(" ")
		for word in word_lst:
			try:
				song_dict[word]
				global song_holder
				song_holder = word
				return True
			except:
				continue
		return False


filter_vulgar = FilterVulgarities()
filter_songs = FilterSongs()

# Functions
def start(bot, update):
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=update.message.chat_id, text="😘😘😘😘😘😘😘😘😘")

def finals_reminder(bot, update):
	rand = random()
	chat_id = update.message.chat_id
	# A 5% chance to give finals reminder
	if rand <= 0.05:
		bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.send_message(chat_id=chat_id, text=finals_reminder_text)
	rand = random()
	# A 2% chance to show you francis' face
	if rand <= 0.02:
		bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		image_rand = randrange(1,15)
		bot.sendPhoto(chat_id=chat_id, photo=open('images/' + str(image_rand) + '.jpg', 'rb'));

	# Add a word per day
	global date_last_added
	global banned_list_custom
	if datetime.date.today() - date_last_added >= 1:
		banned_list_custom.append(RandomWords().random_word())

		

def caps(bot, update, args):
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def vulgarities(bot, update):
	chat_id = update.message.chat_id
	sender = update.message.from_user
	sender_name = str(sender.first_name)
	sender_id = sender.id

	# Increment vulgarity score of user
	try:
		leaderboard[sender_id][0] += 1
		non_vulgarities[sender_id][0] = 0
	except:
		leaderboard[sender_id] = [1, sender_name]
		non_vulgarities[sender_id] = [0, sender_name]

	chosen = randint(0, len(scolding_phrases) - 1)
	bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=chat_id, text=scolding_phrases[chosen] + sender_name + "! " + scolding_emojis[chosen])
	#bot.kick_chat_member(chat_id=chat_id, user_id=update.message.from_user.id)

def say_lyrics(bot, update):
	chat_id = update.message.chat_id
	bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=chat_id, text=song_dict[song_holder])

def show_banned(bot, update):
	chat_id = update.message.chat_id
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	output = "" 
	for word in vulgarity_list:
		output += ("  •  " + word + "\n")
	for word in banned_list_custom:
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
	if (new_word not in banned_list_custom) and (new_word not in vulgarity_list):
		banned_list_custom.append(new_word)
		bot.send_message(chat_id=chat_id, text="New banned word added! 😋")
	else:
		bot.send_message(chat_id=chat_id, text="Word already exist in list! 😒")

def remove_banned(bot, update, args):
	chat_id = update.message.chat_id
	if args:
		rm_word = args[0]
	else:
		bot.send_message(chat_id=chat_id, text="No input, try again.")
		return 		
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	if rm_word in banned_list_custom:
		banned_list_custom.remove(rm_word)
		bot.send_message(chat_id=chat_id, text=rm_word + " removed from banned list!")
	elif rm_word in vulgarity_list:
		bot.send_message(chat_id=chat_id, text="Default banned words cannot be removed! 😤")
	else:	
		bot.send_message(chat_id=chat_id, text="Word does not exist!")

def naughty_list(bot, update):
	chat_id = update.message.chat_id
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	output = "<b>Naughty List:</b>\n"
	sorted_list = sorted(leaderboard, key = lambda x: leaderboard[x][0], reverse = True)
	for i in range(min(len(leaderboard), 10)):
		user = leaderboard[sorted_list[i]]
		output += str(i+1) + ".  " + user[1] + "  |  Score: " + str(user[0]) + "\n"
	bot.send_message(chat_id=chat_id, text=output, parse_mode=telegram.ParseMode.HTML)

def joke(bot, update):
	chat_id = update.message.chat_id
	sender_name = str(update.message.from_user.first_name)
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	bot.send_message(chat_id=chat_id, text="Here's a joke: " + sender_name)

def non_vulgarities(bot, update):
	chat_id = update.message.chat_id
	sender = update.message.from_user
	sender_name = str(sender.first_name)
	sender_id = sender.id

	try:
		non_vulgarities[sender_id][0] -=1
		if non_vulgarities[sender_id][0] = 0
			if leaderboard[sender_id][0] = 1
				leaderboard[sender_id].remove()
			else
				leaderboard[sender_id][0] -= 1
			non_vulgarities[sender_id].remove()
	except:


# Handlers
start_handler = CommandHandler('start', start)
vulgarities_handler = MessageHandler(filter_vulgar, vulgarities)
song_handler = MessageHandler(filter_songs, say_lyrics)
banned_handler = CommandHandler('banned', show_banned)
add_handler = CommandHandler('add', add_banned, pass_args=True)
remove_handler = CommandHandler('remove', remove_banned, pass_args=True)
leaderboard_handler = CommandHandler('naughtyList', naughty_list)
finals_handler = MessageHandler(Filters.text, finals_reminder)
caps_handler = CommandHandler('caps', caps, pass_args=True)
joke_handler = CommandHandler('joke', joke)
non_vulgarities_handler = MessageHandler(,non_vulgarities)

# Dispatching: As soon as you add new handlers to dispatcher, they are in effect.
dispatcher.add_handler(start_handler)
dispatcher.add_handler(remove_handler)
dispatcher.add_handler(banned_handler)
dispatcher.add_handler(vulgarities_handler)
dispatcher.add_handler(song_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(joke_handler)
dispatcher.add_handler(finals_handler)
dispatcher.add_handler(leaderboard_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(non_vulgarities_handler)
	
# Run the bot
updater.start_polling()



"""
bot.send_message(chat_id=update.message.chat_id, text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', parse_mode=telegram.ParseMode.HTML)

Custom keyboard code:
	custom_keyboard = [['top-left', 'top-right'], ['bottom-left', 'bottom-right']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	bot.send_message(chat_id=chat_id, text="Custom Keyboard Test", reply_markup=reply_markup)

"""
