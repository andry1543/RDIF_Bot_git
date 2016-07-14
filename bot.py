# -*- coding: utf-8 -*-
import config
import telebot

bot = telebot.TeleBot(config.token)


#  '/start' and '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Привет!!')


#  '/contacts'.
@bot.message_handler(commands=['contacts'])
def handle_start_contacts(message):
    bot.send_message(message.chat.id, config.contacts)


#  '/info'.
@bot.message_handler(commands=['info'])
def handle_start_info(message):
    bot.send_message(message.chat.id, config.info)


# all other
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    text = 'Что Вы имели в виду, '
    text += message.chat.first_name
    text += '?'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True) 