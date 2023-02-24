import gspread
from oauth2client.service_account import ServiceAccountCredentials

import datetime
import pytz

#P.S. все переоменные назвываем рандомно, но чтоб было удобно, даём правильные имена
#обязательные параметры
scope = ["https://spreadsheets.google.com/feeds", #сами таблицы
         "https://www.googleapis.com/auth/spreadsheets",#АПИ для работы с таблицей
         "https://www.googleapis.com/auth/drive.file", #коннект к гугл-диску
         "https://www.googleapis.com/auth/drive"] #АПИ для авторизации к гугл диску

#подключаем необходимые ключи
creads = ServiceAccountCredentials.from_json_keyfile_name("json_ekaterina.json", scope) #в скобочках указываем название файла json

#авторизируемся под своим аккаунтом из ключа
client = gspread.authorize(creads) #к нему будем обращаться в дальнейшем, т.к. он идёт как подключение

#конец основной части. буду называть её header


#Подключение к таблице, которую мы сами до этого создали
table = client.open('Ekaterina_data_bot') # изменить название на своё
#подключили листы из таблицы
main_list = table.worksheet('main_page') # изменить название листа на своё
question_list = table.worksheet('questions')
other_list = table.worksheet('other')

## ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ
def new_user_add(telegram_id, name, username, number, category, wishes, comments, yes_no, age):
    id = '1_' + f'{len(main_list.col_values(1))}' #вычисляем новый id по колличеству уже имеющихся
    lower_name = name.lower()
    tz_tashkent = pytz.timezone("Asia/Tashkent")
    dt_tashkent =str(datetime.datetime.now(tz_tashkent))
    list_values = [id, telegram_id, lower_name, username, age, number, category, wishes, comments, yes_no,'', dt_tashkent]

    main_list.append_row(list_values)

# СООБЩЕНИЕ в группу при добавлении нового пользователя
def new_user_add_message(username):
    data = main_list.row_values(int(id)+1) # получение значений строки по id

    id = data[0][2:]
    name = data[2]
    username = data[3]
    phone = data[4]
    category = data[5]
    wishes = data[6]
    comment = data[7]
    status = data[8]
    telegram_id = data[1]
    message = f'''  <b>Информация по поиску | ID № {id}:
    ID:</b> {id}
    <b>Имя:</b> <i>{name}</i> | @{username}
    <b>Телефон:</b> {phone}
    <b>Сфера:</b> <i>{category}</i>
    <b>Пожелания:</b> <i>{wishes}</i>
    <b>Комментарий:</b> <i>{comment}</i>
    <b>Статус:</b> <i>{status}</i>

    <b>Telegram id:</b> '{telegram_id}'
'''
    line = [message, telegram_id]
    return line


## СМЕНА СТАТУСА
# смена статуса по ID
def new_status_id(id: str, status: str):
    main_list.update_cell(int(id)+1, 11, status)

# смена статуса по имени
def new_status_name(name:str, status: str):
    cell = main_list.find(name, in_column=3) #получаем значение ячейки с поиском по имени
    main_list.update_cell(cell.row, 11, status)

# смена статуса по username
def new_status_username(username, status):
    cell = main_list.find(username, in_column=4) #получаем значение ячейки с поиском по username
    main_list.update_cell(cell.row, 11, status)


## РАССЫЛКИ
# получение всех telegram-id 
def get_telegram_id_all() -> list:
    data = main_list.col_values(2) # получаем весь список из столбца, включая название
    list_id = list(set(data[1:])) # делаем уникальный список из data, откуда убрали первое значение "название"
   
    return list_id

# получение всех telegram-id с определённой категорией
def get_telegram_id_category(category: str) -> list:
    data = main_list.col_values(2) # получаем список со значением столбца telegram_id
    index = 0 # делаем счетчик для того, чтоб пробегаться по всем строчкам
    list_id = [] # создаём финальный список для всех id
    for i in data: # запускаем цикл по всем значениям столбца с telegram_id
        index += 1 # получаем новую строку для проверки
        check_category = main_list.cell(index, 7).value # получаем категорию по номеру строки

        if check_category == category: # проверяем полученную категорию с искомой
            list_id.append(i) # если совпадает - добавляем telegram_id в финальный спиоск

    return list_id

# получение всех telegram-id с определённым статусом
def get_telegram_id_status(status: str) -> list:
    data = main_list.col_values(2) # получаем список со значением столбца telegram_id
    index = 0 # делаем счетчик для того, чтоб пробегаться по всем строчкам
    list_id = [] # создаём финальный список для всех id
    for i in data: # запускаем цикл по всем значениям столбца с telegram_id
        index += 1 # получаем новую строку для проверки
        check_status = main_list.cell(index, 11).value # получаем статус по номеру строки

        if check_status == status: # проверяем полученный статус с искомым
            list_id.append(i) # если совпадает - добавляем telegram_id в финальный спиоск

    return list_id

# получение всех telegram-id с определённым желанием
def get_telegram_id_wish(status: str) -> list:
    data = main_list.col_values(2) # получаем список со значением столбца telegram_id
    index = 0 # делаем счетчик для того, чтоб пробегаться по всем строчкам
    list_id = [] # создаём финальный список для всех id
    for i in data: # запускаем цикл по всем значениям столбца с telegram_id
        index += 1 # получаем новую строку для проверки
        check_status = main_list.cell(index, 8).value # получаем статус по номеру строки

        if check_status == status: # проверяем полученнон желание  с искомым
            list_id.append(i) # если совпадает - добавляем telegram_id в финальный спиоск

    return list_id



## ОТПРАВКА СООБЩЕНИЯ
# получение одного telegram_id по имени
def get_telegram_id_name(name: str) -> int:
    cell = main_list.find(name) # получение ячейки по поиску
    telegram_id = main_list.cell(cell.row, 2).value # возвращение столбца с telegram_id

    return telegram_id

# получение одного telegram_id по id
def get_telegram_id_id(id: str):
    telegram_id = main_list.cell(int(id)+1, 2).value

    return telegram_id

# получение одного telegram_id по username
def get_telegram_id_username(username: str):
    cell = main_list.find(username, in_column=4)
    telegram_id = main_list.cell(cell.row, 2).value

    return telegram_id



## ПОИСК / получение информации о запросах
# получение запросов по имени
def get_request_name(name: str) -> list:
    find_name = name.lower()
    cell = main_list.find(find_name, in_column=3) # поиск ячейки по имени
    data = main_list.row_values(cell.row) # получение всех значечений строки по ячейке

    id = data[0][2:]
    username = data[3]
    phone = data[4]
    category = data[5]
    wishes = data[6]
    comment = data[7]
    status = data [8]
    telegram_id = data[1]
    message = f'''  <b>Информация по поиску "{name}":</b>
    <b>ID:</b> <i>{id} </i>
    <b>Имя:</b> <i>{name}</i> | @{username}
    <b>Телефон:</b> {phone}
    <b>Сфера:</b> <i>{category}</i>
    <b>Пожелания:</b> <i>{wishes}</i>
    <b>Комментарий:</b> <i>{comment}</i>
    <b>Статус:</b> <i>{status}</i>

    <b>Telegram id:</b> '{telegram_id}'
    '''
    
    line = [message, telegram_id]
    return line

# получение запросов по username
def get_request_username(username: str) -> list:
    cell = main_list.find(username, in_column=4) # поиск ячейки по имени
    data = main_list.row_values(cell.row) # получение всех значечений строки по ячейке

    id = data[0][2:]
    name = data[2]
    username = data[3]
    phone = data[4]
    category = data[5]
    wishes = data[6]
    comment = data[7]
    status = data [8]
    telegram_id = data[1] #нужен, чтоб по этому запросу из БД можно было отправит сообщение напрямую пользователю
    message = f'''  <b>Информация по поиску "{username}":</b>
    <b>ID:</b> <i>{id} </i>
    <b>Имя:</b> <i>{name}</i> | @{username}
    <b>Телефон:</b> {phone}
    <b>Сфера:</b> <i>{category}</i>
    <b>Пожелания:</b> <i>{wishes}</i>
    <b>Комментарий:</b> <i>{comment}</i>
    <b>Статус:</b> <i>{status}</i>

    <b>Telegram id:</b> '{telegram_id}'
'''
    line = [message, telegram_id]
    return line


# получение запросов по id
def get_request_id(id:str) -> list:
    data = main_list.row_values(int(id)+1) # получение значений строки по id

    id = data[0][2:]
    name = data[2]
    username = data[3]
    age = data[4]
    yes_no= data[9]
    phone = data[5]
    category = data[6]
    wishes = data[7]
    comment = data[8]
    status = data[10]
    telegram_id = data[1]
    message = f'''  <b>Информация по поиску | ID № {id}:
    ID:</b> {id}
    <b>Имя:</b> <i>{name}</i> | @{username}
    <b>Опыт с психологом: {yes_no}</b>
    <b>Возарст: {age}</b>
    <b>Телефон:</b> {phone}
    <b>Сфера:</b> <i>{category}</i>
    <b>Пожелания:</b> <i>{wishes}</i>
    <b>Комментарий:</b> <i>{comment}</i>
    <b>Статус:</b> <i>{status}</i>

    <b>Telegram id:</b> '{telegram_id}'
'''
    line = [message, telegram_id]
    return line

# получение запросов по статусу
def get_request_status(status: str) -> list:
    data = main_list.col_values(11) # получение всех статусов
    data = data[1:] # убираем название заголовка
    index = 0 # счетчик для строк
    array = [] # пустой список для финальных сообщений
    for i in data:
        index += 1 # первая и последующие строки
        if i == status: # провекра условия
            info = main_list.row_values(index) # получение значений по строке
            id = info[0][2:]
            name = info[2]
            username = info[3]
            age = info[4]
            yes_no= info[9]
            phone = info[5]
            category = info[6]
            wishes = info[7]
            comment = info[8]
            status = info[10]
            telegram_id = info[1]
            message = f'''  <b>Информация по поиску | ID № {id}:
            ID:</b> {id}
            <b>Имя:</b> <i>{name}</i> | @{username}
            <b>Опыт с психологом: {yes_no}</b>
            <b>Возарст: {age}</b>
            <b>Телефон:</b> {phone}
            <b>Сфера:</b> <i>{category}</i>
            <b>Пожелания:</b> <i>{wishes}</i>
            <b>Комментарий:</b> <i>{comment}</i>
            <b>Статус:</b> <i>{status}</i>

            <b>Telegram id:</b> '{telegram_id}'
            '''

            array.append(message)

    return array

# получение запросов по категории
def get_request_category(category: str) -> list:
    data = main_list.col_values(7)
    data = data[1:]
    index = 0
    array = []
    for i in data:
        index += 1
        if i == category:
            data = main_list.row_values(index)
            id = data[0][2:]
            name = data[2]
            username = data[3]
            age = data[4]
            yes_no= data[9]
            phone = data[5]
            category = data[6]
            wishes = data[7]
            comment = data[8]
            status = data[10]
            telegram_id = data[1]
            message = f'''  <b>Информация по поиску | ID № {id}:
            ID:</b> {id}
            <b>Имя:</b> <i>{name}</i> | @{username}
            <b>Опыт с психологом: {yes_no}</b>
            <b>Возарст: {age}</b>
            <b>Телефон:</b> {phone}
            <b>Сфера:</b> <i>{category}</i>
            <b>Пожелания:</b> <i>{wishes}</i>
            <b>Комментарий:</b> <i>{comment}</i>
            <b>Статус:</b> <i>{status}</i>

            <b>Telegram id:</b> '{telegram_id}'
            '''
            array.append(message)

    return array

## СТАТИСТИКА
# получение колличество пользователей
def get_statistic_users():
    data = main_list.col_values(2)
    data = len(list(set(data[1:])))

    return data

# получение колличество заявок
def get_statistic_request():
    data = main_list.col_values(1)
    data = len(data[1:])

    return data


## РАБОТА С ВОПРОСАМИ

# добавить новый вопрос
def new_question(telegram_id: str, name: str, username: str, question: str):
    id = '2_' + f'{len(question_list.col_values(1))}' #вычисляем новый id по колличеству уже имеющихся
    lower_name = name.lower()
    tz_tashkent = pytz.timezone("Asia/Tashkent")
    dt_tashkent =str(datetime.datetime.now(tz_tashkent))

    list_value = [id, telegram_id, lower_name, username, question, dt_tashkent]

    question_list.append_row(list_value)

# получить вопрос по id
def get_question_new_message() ->list:
    id = len(question_list.col_values(col=1))
    data = question_list.row_values(int(id))

    message = f'Новый вопрос ID№ {data[0]}:\n\nИмя: {data[2]} | @{data[3]}\n\nВопрос:\n{data[4]}\n\nTelegram_id = {data[1]}'
    list_info = [message, data[1]]

    return list_info


# получить вопрос по id
def get_question_id(id: str) ->list:
    data = question_list.row_values(int(id)+1)

    message = f'Поиск вопроса по ID№{data[0]}:\n\nИмя: {data[2]} | @{data[3]}\n\nВопрос:\n{data[4]} \n\nTelegram_id = {data[1]}'
    list_info = [message, data[1]]

    return list_info

# получить вопрос по имени
def get_question_name(name: str):
    lower_name = name.lower()
    cell = question_list.find(lower_name, in_column=3)
    data = question_list.row_values(cell.row)

    message = f'Поиск вопроса по мени: {data[2]}:\n\nID: {data[0][2:]}\nИмя: {data[2]} | @{data[3]}\n\nВопрос:\n{data[4]}'
    list_info = [message, data[1]]

    return list_info

# получить вопрос по username
def get_question_username(username: str):
    cell = question_list.find(username, in_column=4)
    data = question_list.row_values(cell.row)

    message = f'Поиск вопроса по username: {data[2]}:\n\nID: {data[0][2:]}\nИмя: {data[2]} | @{data[3]}\n\nВопрос:\n{data[4]}'
    list_info = [message, data[1]]

    return list_info


## ДРУГОЕ (для кнопок)

# получить все значения колонки "пожелание"
def get_list_wishes():
    data = other_list.col_values(1)
    data = data[1:]

    return data

# получить все значения колонки "возраст"
def get_list_age():
    data = other_list.col_values(2)
    data = data[1:]

    return data

# получить все значения колонки "сфера/категория"
def get_list_category():
    data = other_list.col_values(3)
    data = data[1:]

    return data

# получить все значения колонки "черный список"
def get_black_list():
    data = other_list.col_values(4)
    data = data[1:]

    return data


# получить список админов
def get_admin_list():
    data = other_list.col_values(5)
    data = data[1:]

    return data

# получить колличество запросов
def get_quantity_requests():
    data = main_list.col_values(1)
    data = len(data[1:])

    return data

# получить колличество вопросов
def get_quantity_questions():
    data = question_list.col_values(1)
    data = data[1:]

    return data

# admin получить статусы
def admin_get_status():
    data = other_list.col_values(6)
    data = data[1:]

    return data