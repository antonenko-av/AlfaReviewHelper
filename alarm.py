from modules import myfunc
import config

bot = config.bot
bot.send_message(config.alfa_chat_id, myfunc.review_list(), parse_mode='HTML')
