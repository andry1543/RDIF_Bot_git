# -*- coding: utf-8 -*-

import connection
import sql_queries
import functions

import pymysql.cursors
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def compare(username):
    result = []
    connection_users = pymysql.connect(host=connection.host_portal,
                                       user=connection.user_portal,
                                       password=connection.password_portal,
                                       db=connection.db_portal,
                                       charset=connection.charset,
                                       cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection_users.cursor() as cur_users:
            cur_users.execute(sql_queries.addr_book)

            for row in cur_users:
                mphone = str(row['PERSONAL_MOBILE'])
                wphone = str(row['WORK_PHONE'])
                first_name = str(row['NAME'])
                last_name = str(row['LAST_NAME'])
                first_name_low = first_name.lower()
                last_name_low = last_name.lower()
                find = False
                name = first_name
                name += ' '
                name += last_name
                name_low = name.lower()
                username = functions.transliterate(username)
                username = username.lower()
                rat_name = similar(username, name_low)
                if rat_name > 0.85:
                    row = {'Name': name, 'mobile_phone': mphone, 'work_phone': wphone, 'rat': rat_name}
                    result.clear()
                    result.append(row)
                    break
                elif rat_name > 0.65:
                    if len(result) > 0:
                        find = any(d['Name'] == name for d in result)
                    if not find:
                        row = {'Name': name, 'mobile_phone': mphone, 'work_phone': wphone, 'rat': rat_name}
                        result.append(row)
                    else:
                        find = False
                rat_first_name = similar(username, first_name_low)
                if rat_first_name > 0.8:
                    if len(result) > 0:
                        find = any(d['Name'] == name for d in result)
                    if not find:
                        row = {'Name': name, 'mobile_phone': mphone, 'work_phone': wphone, 'rat': rat_first_name}
                        result.append(row)
                    else:
                        find = False
                rat_last_name = similar(username, last_name_low)
                if rat_last_name > 0.7:
                    if len(result) > 0:
                        find = any(d['Name'] == name for d in result)
                    if not find:
                        row = {'Name': name, 'mobile_phone': mphone, 'work_phone': wphone, 'rat': rat_last_name}
                        result.append(row)
    finally:
        connection_users.close()
        result = sorted(result, key=lambda k: k['rat'], reverse=True)
    return result
