# -*- coding: utf-8 -*-

# Статистика по очередям IT
current_queues = "SELECT queue.name AS 'Queue', " \
                "COUNT(ticket.id) AS '# of tickets' " \
                "FROM ticket " \
                "INNER JOIN queue ON ticket.queue_id = queue.id " \
                "WHERE ticket.queue_id IN ( SELECT id FROM queue WHERE valid_id=1 ORDER BY name) " \
                "AND (ticket.ticket_state_id = 1 OR ticket.ticket_state_id = 4)	" \
                "AND queue.name LIKE 'IT%' " \
                "AND queue.name NOT LIKE '%1C%'" \
                "GROUP BY queue.name;"


# Все задачи агента ОТРС - общая и персональная очереди
detailed_queue = "SELECT queue.name AS 'Queue' " \
                 ",ticket.id AS 'ticket id' " \
                 ",ticket.title AS 'ticket name' " \
                 ",TIMESTAMPDIFF( HOUR, ticket.create_time, CURTIME()) as 'time of life' " \
                 "FROM ticket " \
                 "INNER JOIN " \
                 "queue ON ticket.queue_id = queue.id " \
                 "WHERE (ticket.queue_id = 2 OR ticket.queue_id = %s) " \
                 "AND (ticket.ticket_state_id = 1 OR ticket.ticket_state_id = 4)" \
                 "ORDER BY CAST(TIMESTAMPDIFF( HOUR, ticket.create_time, CURTIME()) AS SIGNED)"


# Проверка пристутсвия пользователя телеграм в базе доверенных.
validation_by_id = "SELECT COUNT(ID) AS 'ID', otrs_queue_id, AD_name, update_time FROM tlgrm_bot.users WHERE ID = %s"


# Update Date update in user DB
update_valid_date = "UPDATE users set update_time = CURDATE() WHERE ID = %s"


# Адресная книга с портала
addr_book = "SELECT NAME, LAST_NAME, PERSONAL_MOBILE, WORK_PHONE " \
            "FROM b_user WHERE ACTIVE LIKE 'Y' " \
            "AND PERSONAL_MOBILE IS NOT NULL " \
            "AND PERSONAL_MOBILE NOT LIKE ''"


# Состояние задач в директуме
directum_state = """
                 SELECT
                 item.Dop3 as 'worker',
                 CASE
                 WHEN [Readed] = 'Y' THEN 'прочтено'
                 WHEN [Readed] = 'N' THEN 'не прочтено'
                 END
                 AS 'read'
                 FROM directum.dbo.SBTaskJob job
                 left join directum.dbo.MBAnalit item on item.Analit = job.Executor
                 WHERE TaskID = %s  AND State = 'W'
                 ORDER BY job.XRecID;
                 """


# Сотрудники в отпуске
otst = "select item.Dop, " \
       "otst.DatClose " \
       "from MBAnalit otst " \
       "left join directum.dbo.MBAnalit item on item.Analit = otst.FIO " \
       "where otst.Vid = (select Vid from MBVidAn where Kod = 'ОТСТ') " \
       "AND otst.DatOpen <  GETDATE() " \
       "AND otst.DatClose >  GETDATE() " \
       "AND otst.StatusOtpuska = 3" \
       "ORDER BY item.Dop;"


# Сотрудники в командировке
komand = "select item.Dop, " \
         "otst.Date3 " \
         "from MBAnalit otst " \
         "left join directum.dbo.MBAnalit item on item.Analit = otst.FIO " \
         "where otst.Vid = (select Vid from MBVidAn where Kod = 'BTBusinessTrips') " \
         "AND otst.Date2 <  GETDATE() " \
         "AND otst.Date3 >  GETDATE() " \
         "AND otst.Proekt != 254247" \
         "AND otst.StateBusinessTrip = 125105" \
         "ORDER BY item.Dop;"
