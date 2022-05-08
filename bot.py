import telebot
from telebot import types

import secret_token
from functions import *


bot = telebot.TeleBot(secret_token.token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, menu_messages.start_menu,
                                      parse_mode='html')
    start_keyboard = types.InlineKeyboardMarkup()
    show_commands = types.InlineKeyboardButton(text='Команды' + '\U0001F4CB	', callback_data='ShowCommands')
    start_keyboard.add(show_commands)
    bot.send_message(message.chat.id, menu_messages.start_button, reply_markup=start_keyboard)


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id, get_menu_from_keys(), parse_mode='html')


@bot.message_handler(content_types=['text'],
func = lambda message: message.text == '/random' or message.text in cocktail_dict.cocktail_name)
def random_cock(message, my_key=get_random_key()):
    if message.text == '/random':
        my_key = get_random_key()
    elif message.text in cocktail_dict.cocktail_name:
        my_key = message.text

    photo = open('photos' + my_key + '.png', 'rb')
    bot.send_photo(message.chat.id, photo, 'Коктейль ' + cocktail_dict.cocktail_name[my_key])
    bot.send_message(message.chat.id, cocktail_dict.cocktail_recipe[my_key], parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text=cocktail_dict.cocktail_name[my_key],
                                             url=cocktail_dict.cocktail_link[my_key])
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, menu_messages.pre_link_button, reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data)
def answer_callback(callback):
    if callback.data == 'ShowCommands':
        bot.send_message(callback.message.chat.id, menu_messages.calback_button,
                                                   parse_mode='html')



bot.polling()
