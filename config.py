# -*- coding: utf-8 -*-


# start phrases for messages
dont_understand = 'Что Вы имели в виду, '
queue = 'Текущее состояние очередей:\n'
q_tot = '\n\nВсего: '


# URLs
otrs_url = 'http://otrs.rdif.local/otrs/index.pl?Action=AgentTicketZoom;TicketID='
rdif_api_url = 'http://api.rdif.ru/vacation/calculator/days/'
xkcd_url = 'http://xkcd.ru/'


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
help_message = '''
Текущие возможности бота:\n
/contacts - Контакты организации
/des Имярек - Поиск рабочего телефона сотрудника РФПИ
/directum 123456 - Проверка состояния задачи в Директум
/info - Информация о боте
/help - Вывод настоящего сообщения
/mob Имярек - Поиск мобильного телефона сотрудника РФПИ
/myid - Возвращает Ваш ID в Telegram
/myqueue - Текущее состояние очереди агнета OTRS
/queue - Текущее состояние очередей IT
/security - Проверка доступа к приватным функциям
/vacation 31.01.2016 - Количество дней отпуска на выбранную дату
               '''

needusername = 'Введите команду в формате: /mob (/des) "имя сотрудника"'
mphoneisempty = "Мобильного телефона нет"
wphoneisempty = "Рабочего телефона нет"

addrbook_empty = "Никого не найдено, попробуйте уточнить поиск"
addrbook_more = "Найдено более пяти человек, если среди них нет нужного Вам, попробуйте уточнить поиск"

directum_state_task = "Задача в работе:\n"
directum_zero_result = "Задача не в работе или не существует"

vacation_fail = "Дата введена в неверном формате, отпуск посчитан на текущую дату: "
vacation_less = "Дата не может быть меньше текущей даты, отпуск посчитан на сегодня: "
vacation_notrfpi = "Вы не являетесь сотрудником РФПИ.\nЗапросите отпуск в своей компании"
vac_days1 = '\nДней отпуска - '
vac_days2 = 'Дней отпуска на '
