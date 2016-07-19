# -*- coding: utf-8 -*-


# start phrases for messages
text = 'Что Вы имели в виду, '
queue = 'Текущее состояние очередей:\n'
q_tot = '\n\nВсего: '


# URLs
otrs_url = 'http://otrs.rdif.local/otrs/index.pl?Action=AgentTicketZoom;TicketID='


# complete messages
start_message = "Привет!!!"
security_fail = "Вы не являетесь зарегистрированным сотрудником РФПИ. Пожалуйста, напишите на" \
                " servicedesk@rdif.ru свой Telegram ID с рабочей почты.\n" \
                "Узнать свой Telegram ID можно с помощью команды '/myid'"
security_success = "You are welcome"
otrs_user_fail = "Извините, но вы не являеттесь агентом OTRS!"
contacts = 'ООО "УК РФПИ"\nwww.rdif.ru\n123317, Пресненская наб., д. 8, стр. 1\nМФК "Город Столиц", ' \
           'Южная башня, 7, 8 этаж\nТелефон: +7 495 644 3414\nФакс: +7 495 644 3413'
info = 'Это бот компании ООО "УК РФПИ"'
help_message = 'Текущие возможности бота:\n\n' \
               '/contacts - Контакты организации\n' \
               '/des - Поиск рабочего телефона сотрудника РФПИ' \
               '/info - Информация о боте\n' \
               '/help - Вывод настоящего сообщения\n' \
               '/mob - Поиск мобильного телефона сотрудника РФПИ' \
               '/myid - Возвращает Ваш ID в Telegram\n' \
               '/myqueue - Текущее состояние очереди агнета OTRS\n' \
               '/queue - Текущее состояние очередей IT\n' \
               '/security - Проверка доступа к приватным функциям\n'
needusername = 'Введите команду в формате: "/mob (/des) имя сотрудника"'
mphoneisempty = "Мобильного телефона нет"
wphoneisempty = "Рабочего телефона нет"
addrbookempty = "Никого не найдено, попробуйте уточнить поиск"
addrbookmore = "Найдено более пяти человек, если среди них нет нужного Вам, попробуйте уточнить поиск"
directum_state_task = "Задача в работе у:\n"
directum_zero_result = "Задача не в работе или не существует"

