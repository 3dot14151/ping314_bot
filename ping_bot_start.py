#!/usr/bin/python
# -*- coding: utf-8

# ИСТОРИЯ:
# 19 Апреля. Наводим красоту. Делает все через процедуры. И регулирование через запуск.
# 15 Июля Добавляем процеду проверки телеграмм клиентов.  
# 15 Июля Запускам все процеду первого запуска. 
# 06 Сентября 2021 - Рассылка информации администраторам.

def telegram_connect (phone_number,api_id,api_hash):         ### Подлючение телеграмм клиента по имени учетки (телефон)
    if phone_number['name'].find ('+') == -1:
        phone_number['name'] = '+'+str(phone_number['name'])
    client = ''
    answer = 'Отсутствует учетная запись в базе'
    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession    
    namebot = 'ping314_bot'
    db,cursor = iz_bot.connect (namebot)   
    sql = "select id,info from accound where name = 'Токен' and data_id = {} limit 1".format(phone_number['id'])
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,info = rec.values()
        session = info
        client = TelegramClient(StringSession(session),api_id=api_id,api_hash=api_hash)
        client.connect()
        if not client.is_user_authorized():
            answer = 'Отсутствует подключение к телеграмм серверу'
        else:
            answer = 'Подключение к телеграмм серверу успешно'
    return client,answer
    
def get_client ():
    import iz_bot
    import random
    namebot = 'ping314_bot'
    db,cursor = iz_bot.connect (namebot)   
    sql = "select id,info as name from accound where name = 'Имя' "
    cursor.execute(sql)
    data = cursor.fetchall()
    random.shuffle(data)
    return data[0]

def get_tasks (setting):  ## Загрузка задания
    import iz_bot
    import random
    db      = setting['db']
    cursor  = setting['cursor']     
    sql = "select id,name,data_id from task where name = 'Имя' and status = ''"
    cursor.execute(sql)
    data = cursor.fetchall()
    random.shuffle(data)
    return data  
    
def get_tasks_setting (task,setting):  ## Загрузка настроек
    element = {}
    db      = setting['db']
    cursor  = setting['cursor']     
    sql = "select id,name,data_id,info from task where data_id = {}".format (task['data_id'])
    cursor.execute(sql)
    data_el = cursor.fetchall()
    for rec_el in data_el: 
        id,name,data_id,info = rec_el.values()  
        element[name] = info
    return element        

def test_cpu_percent (cpu):
    import time
    import psutil
    answer = psutil.cpu_percent(interval=1)
    if answer > 50:
        while answer > 50:
            print ('    [+] 3 * 60 сек')
            time.sleep ( 3 * 60)
            answer = psutil.cpu_percent(interval=1)
    if answer <= 50 and answer > 30:
        print ('    [+] 5 сек')
        time.sleep (5)
    if answer <= 30 and answer > 20:
        print ('    [+] 1 сек')
        time.sleep (1)
    del psutil
    del time
    return answer

def get_command (task,setting): 
    import iz_bot
    db      = setting['db']
    cursor  = setting['cursor']   
    sql = "select id,name,info from service where data_id = {} and status <> 'delete' ".format (task['id'])
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def send_message (client,name,message):                     ## Отправляем сообщение телеграмм боту
    try:
        answer = client.send_message(name,message)
    except:    
        answer = ''
    return answer

def load_message (client,name_bot,limit):
    list = []
    #try:
    next_text = ''
    #if 1==1:
    try:
        message_text = ''
        for message in client.iter_messages(name_bot,limit=limit): 
            next_nomer  = message.id
            message_text   = message.text        
            next_text   = next_text.strip()
            next_message = message
            print ('[+] next_nomer:',next_nomer)
            #list.append([next_nomer,next_text,next_message])
        #telegram_update (client,phone_number)    
    except Exception as e: 
        print ('[-] Ошибка в коде 2:',e)
        answer = 'Ошибка в отправке сообщения'
        return answer
    return message_text 

if __name__ == "__main__":
    import iz_bot
    import time                                                                 ### Получение настроек из базы данных ###  
    import datetime    
    
    set_config  = {'namebot':'ping314_bot'}                                     ## Привязка к базе данных программы
    set_connect = iz_bot.a123_connect (set_config)                              ## Подключение к транзации базы данных
    setting     = iz_bot.a123_get_setting (set_connect)
    api_id      = int(setting.setdefault('api_id',''))
    api_hash    = str(setting.setdefault('api_hash',''))
    setting['Тип основного текста']  = 'Главный'
    setting['Начальный текст']       = 'Запуск проверки работы ботов'
    

    change =[['#Ответ#',str("Нет необходимый данных")],['#Режим#','Начало проверки работы ботов'],['#Пояснение#','Работаем по списку в админке']]
    iz_bot.a123_set_print ('Запуск программы проверки ботов',setting,change)                                                                                ## Информирование администратора о начале работы
    
    
    
    tasks = get_tasks (setting)                                                 ## Получение технического задания
    for task in tasks:
        print ('    [+],Текущая задача: ',task)  
        element     = get_tasks_setting (task,setting)                          ## Объект для работы                   
        commands    = get_command (task,setting)                                ## Список команд для работы с объектом
        answer = 'Отсутствует подключение к телеграмм серверу'

        while answer == 'Отсутствует подключение к телеграмм серверу':          ## Получение активного клиента в телеграмм
            phone_number = get_client ()
            print ('        [+],phone_number',phone_number)
            client,answer = telegram_connect (phone_number,api_id,api_hash)
            time.sleep (3)

        wait_grup = False
        for command in commands:
            print ('        [+] Объект иследования:',element)
            print ('        [+] Команды выполнения:',command)
            message      = command['info']
            name         = command['name']
            namebot      = element['Имя']
            command_id   = task   ['data_id']
            task_id      = task   ['id']
            result       = element['Ожидаемый ответ'] 
            print ('            [+] Имя телеграмм бота:',name)
            
            if name == 'Ожидание':
                print ('    [+] Ожидание ',command['info'])
                time.sleep (int(command['info']))            
            
            if name == 'Задача':                                                                            ## отправляем сообщение телеграмм боту / текст указанный в задании
                answer = send_message (client,namebot,message)                         
            
            if name == 'Просмотреть':    
                from telethon.tl.functions.messages import GetMessagesViewsRequest 
                catalog_name = command['info']             
                messages = client.iter_messages(catalog_name,10)
                list = []
                for message in messages:
                    message_id      = message.id        
                    message_text    = message.text
                    list.append (message_id)
                answer = client(GetMessagesViewsRequest(peer=catalog_name,id=list,increment=True))
                                
            if name == 'Вступить в группу':
                from telethon.tl.functions.channels import JoinChannelRequest
                db,cursor = iz_bot.connect ('ping314_bot')
                catalog_name = command['info'] 
                sql = 'select id,namebot from log where name = "Вступить в группу" and  phone_number = "{}" and namebot = "{}"  limit 1'.format (str(phone_number),catalog_name)
                cursor.execute(sql)
                results = cursor.fetchall()    
                id = 0
                for row in results:
                    id,namebot_v = row.values() 
                if id == 0:
                    answer = client(JoinChannelRequest(catalog_name))
                    print ('    [+] answer:',answer)
                    sql = "INSERT INTO log (`answer`,`namebot`,`name`,`status`,`phone_number`) VALUES (%s,%s,%s,%s,%s)".format ()
                    sql_save =( str(answer),catalog_name,'Вступить в группу','',str(phone_number))
                    cursor.execute(sql,sql_save)
                    db.commit()
                    wait_grup = True
                else:
                    print ('    [+] Пропускаем вступлее. Уже отработана')                
                    
            if name == 'Вступить в группу Ожидание':
                if wait_grup == True:
                    print ('    [+] Ожидание ',command['info'])
                    time.sleep (int(command['info']))
                
            if name == 'Последнее сообщение':                                                  
                answer = load_message (client,namebot,1)
                db      = setting['db']
                cursor  = setting['cursor']  
                sql = "UPDATE task SET info = %s WHERE `name` = 'Полученный ответ' and data_id = %s ".format ()
                sql_save = (answer,command_id)
                cursor.execute(sql,sql_save)
                db.commit() 
                if answer == '/start':
                    message_info = {'namebot':'ping314_bot','user_id':'399838806'}
                    send_data =  {'Text':'Телеграмм бот не отвечает на запросы','Замена':[['#namebot#',namebot],['#result#','OK']]} 
                    iz_bot.send_message (message_info,send_data) 
                if answer == result:
                    message_info = {'namebot':'ping314_bot','user_id':'399838806'}
                    current_time = datetime.datetime.now()
                    print("Time now at greenwich meridian is:", current_time)
                    send_data =  {'Text':'Хороший ответ от бота','Замена':[['#namebot#',namebot],['#result#',str(answer)],['#task_id#',str(task_id)],['#Время#',str(current_time)]]} 
                    iz_bot.send_message (message_info,send_data)
                else:  
                    message_info = {'namebot':'ping314_bot','user_id':'399838806'}
                    send_data =  {'Text':'Изменено приветствие бота','Замена':[['#namebot#',namebot],['#result#',str(result)],['#answer#',str(answer)],['#task_id#',str(task_id)]]} 
                    iz_bot.send_message (message_info,send_data)
                
    import datetime
    now = datetime.datetime.now()
    print("[+]Hour : ",now.hour)
    wait = int(setting.setdefault('Ожидание '+str(now.hour),1200))
    print ('Ожидаем:',int(wait/60),'мин')


    
