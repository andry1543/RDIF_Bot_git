# -*- coding: utf-8 -*-

import config
import connection
import sql_queries
import compare
import functions


import pymssql
import pymysql.cursors
import telebot

bot = telebot.TeleBot(connection.token)


#  '/start' .
@bot.message_handler(commands=['start', 'hi', 'hello', 'привет', 'привет!', 'привет!!'])
def handle_start_help(message):
    bot.send_message(message.chat.id, config.start_message)


#  '/?' and '/help'.
@bot.message_handler(commands=['?', 'help', 'помощь'])
def handle_start_help(message):
    bot.send_message(message.chat.id, config.help_message)


#  '/contacts'. return contacts of RDIF
@bot.message_handler(commands=['contacts', 'контакты'])
def handle_contacts(message):
    bot.send_message(message.chat.id, config.contacts)


# '/joke' Random joke from Bash
@bot.message_handler(commands=['joke', 'bash'])
def handle_joke(message):
    bot.send_message(message.chat.id, functions.getbashquote())


# '/xkcd' Random image from xkcd
@bot.message_handler(commands=['xkcd'])
def handle_joke(message):
    result = functions.getxkcdimage()
    while not result:
        result = functions.getxkcdimage()
    bot.send_photo(message.chat.id, result)


#  '/myid'. return tlgrm id of user
@bot.message_handler(commands=['myid'])
def handle_myid(message):
    bot.send_message(message.chat.id, message.from_user.id)


#  '/mob'. Search mobile in phonebook
@bot.message_handler(commands=['mob', 'моб'])
def handle_abm(message):
    # bot.send_message(message.chat.id, config.needusername)
    if functions.useraccess(message.from_user.id):
        username = message.text[5:]
        i = 0
        if username == "":
            bot.send_message(message.chat.id, config.needusername)
        else:
            result = compare.compare(username)
            if not result:
                bot.send_message(message.chat.id, config.addrbookempty)
            else:
                for row in result:
                    if i > 4:
                        break
                    i += 1
                    name = row['Name']
                    mphone = row['mobile_phone']
                    name += ': '
                    name += mphone
                    if mphone != '':
                        bot.send_message(message.chat.id, name)
                        if i > 4:
                            bot.send_message(message.chat.id, config.addrbookmore)
                    else:
                        bot.send_message(message.chat.id, config.mphoneisempty)
    else:
        bot.send_message(message.chat.id, config.security_fail)


# '/des'. Search workphone in phonebook
@bot.message_handler(commands=['des', 'раб'])
def handle_abw(message):
    # bot.send_message(message.chat.id, config.needusername)
    if functions.useraccess(message.from_user.id):
        username = message.text[5:]
        i = 0
        if username == "":
            bot.send_message(message.chat.id, config.needusername)
        else:
            result = compare.compare(username)
            if not result:
                bot.send_message(message.chat.id, config.addrbookempty)
            else:
                for row in result:
                    if i > 4:
                        break
                    i += 1
                    name = row['Name']
                    wphone = row['work_phone']
                    name += ': '
                    name += wphone
                    if wphone != '':
                        bot.send_message(message.chat.id, name)
                        if i > 4:
                            bot.send_message(message.chat.id, config.addrbookmore)
                    else:
                        bot.send_message(message.chat.id, config.wphoneisempty)
    else:
        bot.send_message(message.chat.id, config.security_fail)


#  '/security'. Test user for security access
@bot.message_handler(commands=['security'])
def handle_security(message):
    if functions.useraccess(message.from_user.id):
        bot.send_message(message.chat.id, config.security_success)
    else:
        bot.send_message(message.chat.id, config.security_fail)


#  '/info'.
@bot.message_handler(commands=['info'])
def handle_info(message):
    bot.send_message(message.chat.id, config.info)


# '/queue'  Statistic of queues
@bot.message_handler(commands=['queue'])
def handle_queue(message):
    connection_otrs = pymysql.connect(host=connection.host_otrs,
                                      user=connection.user_otrs,
                                      password=connection.password_otrs,
                                      db=connection.db_otrs,
                                      charset=connection.charset,
                                      cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection_otrs.cursor() as cur_otrs:
            # Read multiply rows
            total = 0
            cur_otrs.execute(sql_queries.current_queues)
            queue = config.queue
            for row in cur_otrs:
                name = row['Queue']
                num_of_tickets = row['# of tickets']
                total += num_of_tickets
                # print(name)
                ', '.join(row)
                queue += '\n'
                queue += str(name)
                queue += ': '
                queue += str(num_of_tickets)
            queue += config.q_tot
            queue += str(total)
            bot.send_message(message.chat.id, queue)
    finally:
        connection_otrs.close()


# '/myqueue' Details of queues in OTRS for agent
# TODO Need to add basic auth to OTRS.
@bot.message_handler(commands=['myqueue'])
def handle_myqueue(message):
    number = 0
    queue_id = 0
    connection_users = pymysql.connect(host=connection.host_otrs,
                                       user=connection.user_otrs,
                                       password=connection.password_otrs,
                                       db=connection.db_otrs_users,
                                       charset=connection.charset,
                                       cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection_users.cursor() as cur_users:
            cur_users.execute(sql_queries.validation_by_id, message.from_user.id)
            for row in cur_users:
                number = row['ID']
                queue_id = row['otrs_queue_id']
    finally:
        connection_users.close()

    if queue_id == 0 or number != 1:
        bot.send_message(message.chat.id, config.otrs_user_fail)
    else:
        # bot.send_message(message.chat.id, config.security_success)
        connection_otrs = pymysql.connect(host=connection.host_otrs,
                                          user=connection.user_otrs,
                                          password=connection.password_otrs,
                                          db=connection.db_otrs,
                                          charset=connection.charset,
                                          cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection_otrs.cursor() as cur_otrs:
                # Read multiply rows
                total = 0
                cur_otrs.execute(sql_queries.detailed_queue, queue_id)
                url = config.otrs_url
                names = ""
                for row in cur_otrs:
                    url += str(row['ticket id'])
                    lifetime = str(row['time of life'])
                    name = lifetime
                    name += ' ч.  -  <a href="'
                    name += url
                    name += '">'
                    name += str(row['ticket name'])
                    name += '.</a>'
                    total += 1
                    names += name
                    names += '\n'
                    # bot.send_message(message.chat.id, name, True, None, None, 'HTML')
                    url = config.otrs_url
                bot.send_message(message.chat.id, names, True, message.message_id, None, 'HTML')
                bot.send_message(message.chat.id, total)
        finally:
            connection_otrs.close()


# '/directum' Progress of task in the directum
@bot.message_handler(commands=['directum'])
def handle_directum(message):
    if functions.useraccess(message.from_user.id):
        if message.text[10:] != '':
            taskid = message.text[10:]
            if not taskid.isdigit():
                taskid = 0
        else:
            taskid = 0
        connection_directum = pymssql.connect(server=connection.host_directum,
                                              user=connection.user_directum,
                                              password=connection.password_directum,
                                              database=connection.db_directum)
        try:
            with connection_directum.cursor() as cur_directum:
                # Read multiply rows
                cur_directum.execute(sql_queries.directum_state, str(taskid))
                result = config.directum_state_task
                for row in cur_directum:
                    result += str(row[0])
                    result += ', '
                    result += str(row[1])
                    result += '\n'
                if result != config.directum_state_task:
                    bot.send_message(message.chat.id, result)
                else:
                    bot.send_message(message.chat.id, config.directum_zero_result)
        finally:
            connection_directum.close()


# all other
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    text = config.text
    text += message.from_user.first_name
    text += '?'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)