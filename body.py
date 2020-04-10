import telebot
from modules import myfunc
import config

# keyboard
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Файлы на ревью')


# Telegramm token
bot = config.bot

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет, я Кира. Меня создали, чтобы помочь дизайнерам не забывать о том, сколько файлов сейчас находится на ревью. В будущем, я буду напоминать о новых проектах и собирать статистику.")
	bot.send_message(message.chat.id, 'Для того, чтобы получить список файлов проходящих ревью, напиши /files в чат или нажми на кнопку', reply_markup=keyboard1)
	print (message)
@bot.message_handler(commands=['files'])
def handle_message(message):
	message_to = myfunc.review_list()
	bot.send_message(message.chat.id, message_to, parse_mode='HTML')

@bot.message_handler(content_types=['text'])
def handle_message(message):
	if message.text.lower() == 'файлы на ревью':
		text = myfunc.review_list()
		bot.send_message(message.chat.id, text, parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, 'Для того, чтобы получить список файлов, напиши /files в чат или нажми на кнопку',reply_markup=keyboard1)



bot.polling()

