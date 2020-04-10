import requests
import datetime
from telebot import types
import config


# Telegramm token
bot = config.bot

#variables
files_list = {}

def response():
    # set variables for Figma API
    API_TOKEN = config.figma_api_token
    url = config.url_review_project
    headers = {'X-FIGMA-TOKEN': API_TOKEN}

    # make call for JSON and process it
    resp = requests.get(url, headers=headers)
    json_response = resp.json()
    node_list = json_response.get("files")

    return node_list

def review_list():
    node_list = response()

    now_date = datetime.datetime.now()
    message_to = 'Файлы на ревью:\n\n'

    for i in node_list:
        last_modified_date = i["last_modified"]
        file_date = last_modified_date.split('T')
        date_string = file_date[0].split('-')
        then = datetime.datetime(int(date_string[0]), int(date_string[1]), int(date_string[2]))
        delta = now_date - then
        if delta.days == 0:
            message_to = message_to + '<b>' + i["name"] +'</b>' + "\n" + 'Обновлено сегодня' + "\n" + "\n"
        else:
            message_to = message_to + '<b>' + i["name"] +'</b>' + "\n" + 'Дней без обновлений: ' + str(delta.days) + "\n" + "\n"
    return message_to

def update ():
    node_list = response()

# Заполняем словарь
    for i in node_list:
            global files_list
            files_list[i["key"]] = i["name"], i["last_modified"]
    print('База обновлена')

def search():
    node_list = response()

    for i in node_list:
        if i['key'] in files_list:
            pass
        else:
            files_list[i["key"]] = i["name"], i["last_modified"]

            file_url = i['key']
            file_url = 'https://figma.com/file/' + file_url
            markup = types.InlineKeyboardMarkup()
            btn_figma = types.InlineKeyboardButton(text='Открыть файл', url=file_url)
            markup.add(btn_figma)

            bot.send_message(config.alfa_chat_id, 'Новый файл: \n' + '<b>' + str(i['name']) + '</b>', reply_markup = markup, parse_mode='HTML')

def whats_new (text):
    bot.send_message(config.alfa_chat_id, text, parse_mode='HTML')