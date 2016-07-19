# -*- coding: utf-8 -*-
import json
import requests
import pymysql.cursors
import urllib.request
import random


import connection
import sql_queries


# Транслитерация
def transliterate(string):

    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'Ж': u'Zh',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ц': u'Ts',
                       u'Ч': u'Ch',
                       u'Ш': u'Sh',
                       u'Щ': u'Sch',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E',
                       u'Ю': u'Yu',
                       u'Я': u'Ya',}

    lower_case_letters = {u'а': u'a',
                          u'б': u'b',
                          u'в': u'v',
                          u'г': u'g',
                          u'д': u'd',
                          u'е': u'e',
                          u'ё': u'e',
                          u'ж': u'zh',
                          u'з': u'z',
                          u'и': u'i',
                          u'й': u'y',
                          u'к': u'k',
                          u'л': u'l',
                          u'м': u'm',
                          u'н': u'n',
                          u'о': u'o',
                          u'п': u'p',
                          u'р': u'r',
                          u'с': u's',
                          u'т': u't',
                          u'у': u'u',
                          u'ф': u'f',
                          u'х': u'h',
                          u'ц': u'ts',
                          u'ч': u'ch',
                          u'ш': u'sh',
                          u'щ': u'sch',
                          u'ъ': u'',
                          u'ы': u'y',
                          u'ь': u'',
                          u'э': u'e',
                          u'ю': u'yu',
                          u'я': u'ya',}

    translit_string = ""

    for index, char in enumerate(string):
        if char in lower_case_letters:
            char = lower_case_letters[char]
        elif char in capital_letters.keys():
            char = capital_letters[char]
            if len(string) > index+1:
                if string[index+1] not in lower_case_letters:
                    char = char.upper()
            else:
                char = char.upper()
        translit_string += char

    return translit_string


# Сверка пользователя с базой SQL
def useraccess(userid):
    number = 0
    connection_users = pymysql.connect(host=connection.host_otrs,
                                       user=connection.user_otrs,
                                       password=connection.password_otrs,
                                       db=connection.db_otrs_users,
                                       charset=connection.charset,
                                       cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection_users.cursor() as cur_users:
            cur_users.execute(sql_queries.validation_by_id, userid)
            for row in cur_users:
                number = row['ID']
    finally:
        connection_users.close()
    if number != 1:
        return False
    else:
        return True


'''
Модуль, получающий случайные цитаты с сайта bash.im.
Т.к. парсить сам Баш долго и нудно, предлагаю использовать мой промежуточный сервер.
В его БД хранятся все цитаты на сегодняшний день.
Модуль взят у Groosha
'''


def getbashquote():
    url = 'http://pebble.groosh.pw/nget.php'
    params = dict(
        quote=0
    )

    resp = requests.get(url=url, params=params)
    try:
        data = json.loads(resp.text.replace('\x00', ''))
        text = data['text'].replace('<br />', '\n')\
            .replace('&quot;', '\"')\
            .replace('<br>', '\n')
        return str(data['id']).replace('#', '№') + '\n' + text
    except Exception:
        return 'bash: Произошла ошибка, попробуйте ещё раз'


def getxkcdimage():
    number = random.randint(1, 1582)
    url = 'http://xkcd.ru/i/'
    url += str(number)
    url += '_v'
    url_while = url
    i = 9
    while i > 0:
        url_while += str(i)
        url_while += '.png'
        i -= 1
        try:
            urllib.request.urlopen(url_while)
            url = url_while
            f = open('out.png', 'wb')
            f.write(urllib.request.urlopen(url_while).read())
            f.close()
            img = open('out.png', 'rb')
            return img
        except urllib.request.HTTPError:
            pass
        url_while = url
    return False


