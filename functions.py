# -*- coding: utf-8 -*-


import pymysql.cursors
import urllib.request as urllib2
from bs4 import BeautifulSoup
import datetime
import ldap3
import random


import connection
import sql_queries
import config


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
                       u'Я': u'Ya'}

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
                          u'я': u'ya'}

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


# Check user in SQL and AD
def useraccess(userid):
    server = ldap3.Server(connection.ad_server, get_info=ldap3.ALL)
    conn = ldap3.Connection(server,
                            user=connection.ad_user,
                            password=connection.ad_secret,
                            authentication=ldap3.NTLM)
    number = 0
    user = ''
    update_time = 0
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
                user = row['AD_name']
                update_time = row['update_time']
    finally:
        connection_users.close()
    if number != 1:
        return False
    elif datetime.date.today() - datetime.timedelta(days=7) > update_time:
        conn.bind()
        if conn.search(search_base=connection.ad_ou,
                       search_filter='(&(samAccountName=' + user + '))'):
            connection_users = pymysql.connect(host=connection.host_otrs,
                                               user=connection.user_otrs,
                                               password=connection.password_otrs,
                                               db=connection.db_otrs_users,
                                               charset=connection.charset,
                                               cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection_users.cursor() as cur_users:
                    cur_users.execute(sql_queries.update_valid_date, userid)
                    connection_users.commit()
            finally:
                cur_users.close()
                connection_users.close()
            conn.unbind()
            return True
        else:
            conn.unbind()
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

    number = random.randint(1, 1000000)

    bash_text = ""
    url = config.bash_url + str(number)

    request = urllib2.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) "
                                                          "Gecko/20100101 Firefox/40.0"})

    try:
        resp = urllib2.urlopen(request)
        if resp.url == 'http://bash.im/':
            return False
    except urllib2.HTTPError:
        return 'bash: Произошла ошибка, попробуйте ещё раз'

    web_soup = BeautifulSoup(resp, "html.parser")
    bash_tag = web_soup.find(name="div", attrs={'class': 'text'})
    for string in bash_tag.strings:
        bash_text += string + "\n"
    return '№' + str(number) + '\n' + bash_text


def getxkcdimage():
    number = random.randint(1, 1582)
    xkcd_url = config.xkcd_url + str(number)
    try:
        web_soup = BeautifulSoup(urllib2.urlopen(xkcd_url),  "html.parser")
    except urllib2.HTTPError:
        return False, False

    xkcd_urlimg = web_soup.find(name="img")["src"]
    xkcd_text = web_soup.find(name="div", attrs={'class': 'comics_text'})
    try:
        urllib2.urlopen(xkcd_urlimg)
        f = open('out.png', 'wb')
        f.write(urllib2.urlopen(xkcd_urlimg).read())
        img = open('out.png', 'rb')
        f.close()
        return img, xkcd_text
    except urllib2.HTTPError:
        pass
    return False, False


# get quantity of free days from 1C through web api
def getvacation(userid, date):
    server = ldap3.Server(connection.ad_server, get_info=ldap3.ALL)
    conn = ldap3.Connection(server,
                            user=connection.ad_user,
                            password=connection.ad_secret,
                            authentication=ldap3.NTLM)
    number = 0
    user = ''
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
                user = row['AD_name']

    finally:
        connection_users.close()
    if number != 1:
        return False
    else:
        conn.bind()
        try:
            conn.search(search_base=connection.ad_ou,
                        search_filter='(&(samAccountName=' + user + '))',
                        attributes=['extensionAttribute10'])
            entry = conn.entries[0]
            onesid = entry['extensionAttribute10']
        except ldap3.LDAPKeyError:
            return -5001
        finally:
            conn.unbind()
        url = config.rdif_api_url + str(onesid) + '&date=' + str(date)
        try:
            days = int(urllib2.urlopen(url).read())
        except urllib2.HTTPError:
            return False
        return days
