import telebot
from telebot import types

import ekaterina_buttons
import ekaterina_data
from config import TOKEN, GROUP_ID

import datetime
import time
import pytz

import text_messages



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['admin'])
def start_check_admin(message):
    admin_list = ekaterina_data.get_admin_list()

    if str(message.from_user.id) in admin_list:
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)

    else:
        bot.send_message(message.from_user.id, 'Команда не разспознана, попробуйте другую')
#### ГЛАВНОЕ МЕНЮ
def admin_check_command(message):
    command = message.text
    command_list = ['Запросы', 'Вопросы', 'Статистика', 'Рассылка']
    if command in command_list:

        if command == command_list[0]:
            bot.send_message(
                            message.from_user.id,
                            'Выберите действие с Запросами',
                            reply_markup=ekaterina_buttons.admin_get_requests()
                            )
            bot.register_next_step_handler(message, admin_requests_menu)

        elif command == command_list[1]:
            bot.send_message(
                            message.from_user.id,
                            'Выберите действие с Вопросами',
                            reply_markup=ekaterina_buttons.admin_get_question()
                            )
            bot.register_next_step_handler(message, admin_question_menu)

        elif command == command_list[2]:
            bot.send_message(
                            message.from_user.id,
                            'Какую статистику вы хотите узнать?',
                            reply_markup=ekaterina_buttons.admin_get_statistics()
                            )
            bot.register_next_step_handler(message, admin_statistics_menu)

        elif command == command_list[3]:
            bot.send_message(
                            message.from_user.id,
                            'Выберите, кому хотите отрпавить рассылку',
                            reply_markup=ekaterina_buttons.admin_mailng_main()
                            )
            bot.register_next_step_handler(message, admin_send_mailing)

        else:
            bot.send_message(
                            message.from_user.id,
                            '''Команда не найдена. \nПопробуйте еще раз 
                            или свяжитесь с разработчиком бота''')
            bot.register_next_step_handler(message, admin_check_command)

    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, попробуйте другую', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)

# ГЛАВНОЕ МЕНЮ - ЗАПРОСЫ
def admin_requests_menu(message):
    command = message.text
    command_list = ['Получить запрос по ID', 'Получить запрос по имени', 'Получить запрос по username', 'Получить запрос по статусу', 'Получить запрос по сфере/категории', 'Назад', 'Отмена']

    if command in command_list:
        if command == 'Получить запрос по ID':
            data = len(ekaterina_data.get_quantity_requests())
            bot.send_message(
                            message.from_user.id, 
                            f'Введите/выберите ID (номер) запроса\nКоличество запросов: {data}',
                            reply_markup=ekaterina_buttons.admin_get_quantity_requests_inline(),
                            )
            bot.send_message(message.from_user.id, 'Отправить ему оповещениие?', reply_markup=ekaterina_buttons.admin_send_message_inline())
            bot.register_next_step_handler(message, admin_request_id_action_message)

        elif command == 'Получить запрос по имени':
            bot.send_message(
                            message.from_user.id, 
                            'Введите имя для начала поиска',
                            reply_markup=ekaterina_buttons.cancel()
                            )
            bot.register_next_step_handler(message, admin_request_name)
        elif command == 'Получить запрос по username':
            bot.send_message(
                            message.from_user.id,
                            'Введите username для начала поиска',
                            reply_markup=ekaterina_buttons.cancel()
                            )
            bot.register_next_step_handler(message, admin_request_username)
        
        elif command == 'Получить запрос по статусу':
            bot.send_message(
                            message.from_user.id,
                            'Введите статус для начала поиска',
                            reply_markup=ekaterina_buttons.cancel()
                            )
            bot.register_next_step_handler(message, admin_request_satatus)

        elif command == 'Получить запрос по сфере/категории':
            bot.send_message(
                            message.from_user.id,
                            'Введите сферу, по которой будет вестись поиск',
                            reply_markup=ekaterina_buttons.cancel()
                            )
            bot.register_next_step_handler(message, admin_request_category)
            

        elif command == 'Назад' or command == 'Отмена':
            bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_main())
            bot.register_next_step_handler(message, admin_check_command)
    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, попробуйте другую или можете вернуться в главное меню', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_requests_menu)

# ГЛАВНОЕ МЕНЮ - ЗАПРОСЫ - по иммени
def admin_request_name(message):
    name = message.text
    data = ekaterina_data.get_request_name(name)
    bot.send_message(message.from_user.id, data[0], reply_markup=ekaterina_buttons.admin_send_message(), parse_mode='html')
    bot.register_next_step_handler(message, admin_request_name_action, data)

def admin_request_name_action(message, data):
    command = message.text

    if command == 'Отправить сообщение':
        bot.send_message(message.from_user.id, 'Отправьте сообщение пользователю', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_request_name_action_message, data)
    elif command == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите действие с запросами', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)
    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, начните с начала', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)

def admin_request_name_action_message(message, data):
    text = message.text

    bot.send_message(data[1], text)
    bot.send_message(message.from_user.id, 'Сообщение успешно доставлено пользователю \nВыберите действие', reply_markup=ekaterina_buttons.admin_main())
    bot.register_next_step_handler(message, admin_check_command)

# ГЛАВНОЕ МЕНЮ - ЗАПРОСЫ - по username
def admin_request_username(message):
    username = message.text
    username = username.strip()

    if username[0] == '@':
        data = ekaterina_data.get_request_username(username[1:])
        bot.send_message(message.from_user.id, data[0], reply_markup=ekaterina_buttons.admin_send_message(), parse_mode='html')
        bot.register_next_step_handler(message, admin_request_username_action, data)
    else:
        data = ekaterina_data.get_request_username(username)
        bot.send_message(message.from_user.id, data[0], reply_markup=ekaterina_buttons.admin_send_message(), parse_mode='html')
        bot.register_next_step_handler(message, admin_request_username_action, data)

def admin_request_username_action(message, data):
    command = message.text

    if command == 'Отправить сообщение':
        bot.send_message(message.from_user.id, 'Отправьте сообщение пользователю', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_request_username_action_message, data)
    elif command == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите действие с запросами', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)
    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, начните с начала', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)

def admin_request_username_action_message(message, data):
    text = message.text

    bot.send_message(data[1], text)
    bot.send_message(message.from_user.id, 'Сообщение успешно доставлено пользователю \nВыберите действие', reply_markup=ekaterina_buttons.admin_main())
    bot.register_next_step_handler(message, admin_check_command)


# ГЛАВНОЕ МЕНЮ - ЗАПРОСЫ - по id
def admin_request_id_action(message):
    command = message.text

    if command == 'Отправить сообщение':
        bot.send_message(message.from_user.id, 'Введите telegram_id пользователя', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_request_id_action_message)
    elif command == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите действие с запросами', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)
    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, начните с начала', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)

def admin_request_id_action_message(message):
    text = message.text
    if text.isdigit():
        telegram_id = message.text
        telegram_id = telegram_id.strip()
        telegram_id = int(telegram_id)

        bot.send_message(message.from_user.id, 'Введите текст сообщения', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_request_id_action_send_message, telegram_id)
    elif not text.isdigit():
        bot.send_message(message.from_user.id, 'Выберите команду', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)

def admin_request_id_action_send_message(message, telegram_id):
    text = message.text

    bot.send_message(telegram_id, text)
    bot.send_message(message.from_user.id, 'Сообщение доставлено', reply_markup=ekaterina_buttons.admin_main())
    bot.register_next_step_handler(message, admin_check_command)


# ГЛАВНОЕ МЕНЮ - ЗАПРОСЫ - по статусу
def admin_request_satatus(message):
    
    if message.text == 'Отмена':
        bot.send_message(message.from_user.id, 'Выберите действие с запросами', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)
    else:
        status = message.text
        data = ekaterina_data.get_request_status(status=status)

        bot.send_message(message.from_user.id, data, parse_mode='html', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)


# ГЛАВНОЕ МЕНЮ - ЗАПРОСЫ - по категории/сфере
def admin_request_category(message):
    
    if message.text == 'Отмена':
        bot.send_message(message.from_user.id, 'Выберите действие с запросами', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)
    else:
        category = message.text
        data = ekaterina_data.get_request_category(category)
        bot.send_message(message.from_user.id, data, parse_mode='html', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)


# ГЛАВНОЕ МЕНЮ - ВОПРОСЫ
def admin_question_menu(message):
    command = message.text

    command_list = ['Получить вопрос по ID', 'Получить вопрос по имени', 'Получить вопрос по username', 'Назад', 'Отмена']

    if command in command_list:
        if command == 'Получить вопрос по ID':
            quantity = len(ekaterina_data.get_quantity_questions())
            bot.send_message(message.from_user.id, f'Выберите ID для получения вопроса\n\nКолличество вопросов: {quantity}', reply_markup=ekaterina_buttons.admin_get_quantity_question_inline())
            bot.send_message(message.from_user.id, 'Ответить на вопрос', reply_markup=ekaterina_buttons.admin_answer_question_inline())
            bot.register_next_step_handler(message, admin_question_id)
        elif command == 'Получить вопрос по имени':
            bot.send_message(message.from_user.id, 'Введите имя для поиска')
            bot.register_next_step_handler(message, admin_question_name)
        elif command == 'Получить вопрос по username':
            bot.send_message(message.from_user.id, 'Введите username для поиска')
            bot.register_next_step_handler(message, admin_question_username)
        elif command == 'Назад' or command == 'Отмена':
            bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_main())
            bot.register_next_step_handler(message, admin_check_command)
    else:
        bot.send_message(
                        message.from_user.id,
                        'Введена неизвестная команда, давайте начнём сначала',
                        reply_markup=ekaterina_buttons.admin_main()
                        )
        bot.register_next_step_handler(message, admin_check_command)


# ГЛАВНОЕ МЕНЮ - ВОПРОСЫ - по id
def admin_question_id(message):
    text = message.text
    text = text.split()

    if text[0].isdigit():
        telegram_id = text
        bot.send_message(message.from_user.id, 'Отправьте текст ответа', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_question_id_answer, telegram_id)
    else:
        bot.send_message(message.from_user.id, 'Выберите следующее действие', reply_markup=ekaterina_buttons.admin_get_question())
        bot.register_next_step_handler(message, admin_question_id)

def admin_question_id_answer(message, telegram_id):
    text = message.text

    if text == 'Отмена':
        bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=ekaterina_buttons.admin_get_question())
        bot.register_next_step_handler(message, admin_question_menu)
    else:
        bot.send_message(int(telegram_id[0]), text)
        bot.send_message(message.from_user.id, 'Ответ на вопрос отправлен успешно!\n\nВыбереите следующее действие', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)


# ГЛАВНОЕ МЕНЮ - ВОПРОСЫ - по имени
def admin_question_name(message):
    name = message.text

    info = ekaterina_data.get_question_name(name)
    bot.send_message(message.from_user.id, info[0], reply_markup=ekaterina_buttons.admin_send_message())
    bot.register_next_step_handler(message, admin_question_name_action, info)

def admin_question_name_action(message, info):
    command = message.text

    if command == 'Отправить сообщение':
        bot.send_message(message.from_user.id, 'Введите текст ответа на вопрос', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_question_name_send, info)
    elif command == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите дейсвтвие', reply_markup=ekaterina_buttons.admin_get_question())
        bot.register_next_step_handler(message, admin_question_menu)

def admin_question_name_send(message, info):
    answer = message.text

    if answer == 'Отмена':
        bot.send_message(message.from_user.id, 'Выберите дейсвтие', reply_markup=ekaterina_buttons.admin_get_question())
        bot.register_next_step_handler(message, admin_question_menu)
    else:
        bot.send_message(int(info[1]), answer)
        bot.send_message(message.from_user.id, 'Ответ успешно отправлен', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)


# ГЛАВНОЕ МЕНЮ - ВОПРОСЫ - по username
def admin_question_username(message):
    username = message.text

    if username[0] == '@':
        data = ekaterina_data.get_question_username(username[1:])
        bot.send_message(message.from_user.id, data, reply_markup=ekaterina_buttons.admin_send_message())
        bot.register_next_step_handler(message, admin_question_username_action, data)
    elif username[0] != '@':
        data = ekaterina_data.get_question_username(username)
        bot.send_message(message.from_user.id, data, reply_markup=ekaterina_buttons.admin_send_message())
        bot.register_next_step_handler(message, admin_question_username_action, data)

def admin_question_username_action(message, data):
    command = message.text

    if command == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите дейсвтие', reply_markup=ekaterina_buttons.admin_get_question())
        bot.register_next_step_handler(message, admin_question_menu)
    
    elif command == 'Отправить сообщение':
        bot.send_message(message.from_user.id, 'Введите сообщение', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_question_username_send, data)

def admin_question_username_send(message, data):
    text = message.text

    if text == 'Отмена':
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_get_question())
        bot.register_next_step_handler(message, admin_question_menu)

    else:
        bot.send_message(int(data[1]), text)
        bot.send_message(message.from_user.id, 'Ответ на сообщение отправлен', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)
    

# ГЛАВНОЕ МЕНЮ - СТАТИСТИКА
def admin_statistics_menu(message):
    command = message.text
    command_list = ['Количество заявок', 'Количество пользователей', 'Назад', 'Отмена']

    if command in command_list:
        if command == 'Количество заявок':
            data = ekaterina_data.get_statistic_request()
            bot.send_message(message.from_user.id, data, reply_markup=ekaterina_buttons.admin_main())
            bot.register_next_step_handler(message, admin_check_command)
        elif command == 'Количество пользователей':
            data = ekaterina_data.get_statistic_users()
            bot.send_message(message.from_user.id, data, reply_markup=ekaterina_buttons.admin_main())
            bot.register_next_step_handler(message, admin_check_command)
        elif command == 'Назад' or command == 'Отмена':
            bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_main())
            bot.register_next_step_handler(message, admin_check_command)
    else:
        bot.send_message(message.from_user.id, 'Введена неизвестная команда, попробуйте снова или свяжитесь с разработчиком', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)


# ГЛАВНОЕ МЕНЮ - РАССЫЛКА
def admin_send_mailing(message):
    command = message.text

    command_list = ['Категории/Сфера', 'Пожелания', 'Всем', 'Отмена', 'Назад',]

    if command in command_list:

        if command == 'Категории/Сфера':
            bot.send_message(message.from_user.id, 'Выберите категорию, по которой вы отправите рассылку', reply_markup=ekaterina_buttons.admin_category())
            bot.register_next_step_handler(message, admin_send_mailing_category)
        elif command == 'Пожелания':
            bot.send_message(message.from_user.id, 'Выберите пожелание, по которой отправите рассылку', reply_markup=ekaterina_buttons.admin_wishes())
            bot.register_next_step_handler(message, admin_send_mailing_wishes)
        elif command == 'Статус':
            bot.send_message(message.from_user.id, 'Выберите статус пользователей, по которой отправите рассылку', reply_markup=ekaterina_buttons.adm())
            bot.register_next_step_handler(message, admin_send_mailing_status)
        elif command == 'Всем':
            bot.send_message(message.from_user.id, 'Введите текст сообщения для отправки всем пользователям', reply_markup=ekaterina_buttons.cancel())
            bot.register_next_step_handler(message, admin_send_meiling_everyone)
        elif command == 'Назад':
            bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_main())
            bot.register_next_step_handler(message, admin_check_command)

    else:
        bot.send_message(message.from_user.id, 'Введена не существующая команда, попробуйте снова', reply_markup=ekaterina_buttons.admin_mailng_main())
        bot.register_next_step_handler(message, admin_send_mailing)


# ГЛАВНОЕ МЕНЮ - РАССЫЛКА - по категориям/сферы
def admin_send_mailing_category(message):
    command_list = ekaterina_data.get_list_category()
    command = message.text

    if command in command_list:
        bot.send_message(message.from_user.id, 'Введите текст для расслыки', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_send_mailing_category_action, command)
    elif command == 'Отмена' or command == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите дейсвтие', reply_markup=ekaterina_buttons.admin_mailng_main())
        bot.register_next_step_handler(message, admin_send_mailing)
    else:
        bot.send_message(message.from_user.id, 'Введена неизвестная команда, попробуйте снова', reply_markup=ekaterina_buttons.admin_mailng_main())
        bot.register_next_step_handler(message, admin_send_mailing)

def admin_send_mailing_category_action(message, command):
    telegram_id_list = ekaterina_data.get_telegram_id_category(category=command)
    text = message.text
    for i in telegram_id_list:
        bot.send_message(int(i), text)
        time.sleep(0.2)
    bot.send_message(message.from_user.id, 'Рассылка отправлена успешно', reply_markup=ekaterina_buttons.admin_mailng_main())
    bot.register_next_step_handler(message, admin_send_mailing)

# ГЛАВНОЕ МЕНЮ - РАССЫЛККА - пожелания
def admin_send_mailing_wishes(message):
    command = message.text
    command_list = ekaterina_data.get_list_wishes()

    if command in command_list:
        bot.send_message(message.from_user.id, 'Введите текст сообщения', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_send_mailing_wishes_action, command)
    elif command == 'Отмена' or command == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_mailng_main())
        bot.register_next_step_handler(message, admin_send_mailing)
    else:
        bot.send_message(message.from_user.id, 'Введена неизвестная команда, попробуйте снова', reply_markup=ekaterina_buttons.admin_mailng_main())
        bot.register_next_step_handler(message, admin_send_mailing)
    
def admin_send_mailing_wishes_action(message, command):
    text = message.text
    telegram_list = ekaterina_data.get_telegram_id_wish(text)

    for id in telegram_list:
        bot.send_message(int(id), text)
        time.sleep(0.2)

    bot.send_message(message.from_user.id, 'Рассылка отправлена успешно', reply_markup=ekaterina_buttons.admin_mailng_main())
    bot.register_next_step_handler(message, admin_send_mailing())


# ГЛАВНОЕ МЕНЮ - РАССЫЛКА - статус
def admin_send_mailing_status(message):
    status = message.text
    telegram_id_list= ekaterina_data.get_telegram_id_status(status)
    if message.text == 'Отмена' or message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_mailng_main())
        bot.register_next_step_handler(message, admin_send_mailing)
    else:
        bot.send_message(message.from_user.id, 'Введите текст сообщения', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_send_mailing_status_action, telegram_id_list)
    
def admin_send_mailing_status_action(message, telegram_id_list):
    text = message.text


    for id in telegram_id_list:
        bot.send_message(int(id), text)
        time.sleep(0.2)

    bot.send_message(message.from_user.id, 'Рассылка отправлена успешно', reply_markup=ekaterina_buttons.admin_mailng_main())
    bot.register_next_step_handler(message, admin_send_mailing)

# ГЛАВНОЕ МЕНЮ - РАССЫЛКА - всем
def admin_send_meiling_everyone(message):
    bot.send_message(message.from_user.id, 'Введите текст сообщения', reply_markup=ekaterina_buttons.cancel())
    bot.register_next_step_handler(message, admin_send_meiling_everyone_action, )
    if message.text == 'Отмена' or message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.admin_mailng_main())
        bot.register_next_step_handler(message, admin_send_mailing)
    
def admin_send_meiling_everyone_action(message, command):
    text = message.text
    telegram_list = ekaterina_data.get_telegram_id_all()

    for id in telegram_list:
        bot.send_message(int(id), text)
        time.sleep(0.2)

    bot.send_message(message.from_user.id, 'Рассылка отправлена успешно', reply_markup=ekaterina_buttons.admin_mailng_main())
    bot.register_next_step_handler(message, admin_send_mailing())
#---#---#---#---#---#---#---#---#---
#---#---#---#---#---#---#---#---#---#---#---#---
#---#---#---#---#---#---#---#---#---#---#---#---




@bot.message_handler(commands=['start', 'help'])
def user_check_black_list(message):
    black_list = ekaterina_data.get_black_list()

    telegram_id = str(message.from_user.id)

    if telegram_id in black_list:
        bot.send_message(message.from_user.id, 'Бот не доступен. Свяжитесь с нами по номеру телефона: ...')
    else:
        bot.send_message(message.from_user.id, text=text_messages.START_MESSAGE, reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)


# ГЛАВНОЕ МЕНЮ (обработчик команд)
def user_check_command(message):
    command_list = ['Записаться на консультацию', 'Задать вопрос', 'Обо мне', 'Мои соц.сети']
    command = message.text
    if message.text in command_list:
        if command == 'Записаться на консультацию':
            bot.send_message(message.from_user.id, text_messages.TAKE_REQUEST_1)
            bot.send_message(message.from_user.id, text=text_messages.TAKE_REQUEST_1_1, reply_markup=ekaterina_buttons.user_yes_no())
            bot.register_next_step_handler(message, user_get_request)
        elif command == 'Задать вопрос':
            bot.send_message(message.from_user.id, text=text_messages.ASK_QUESTION, reply_markup=ekaterina_buttons.cancel())
            bot.register_next_step_handler(message, user_get_question_body)
        elif command == 'Обо мне':
            bot.send_message(message.from_user.id, text_messages.ABOUT_ME, reply_markup=ekaterina_buttons.user_main())
            bot.register_next_step_handler(message, user_check_command)
        elif command == 'Мои соц.сети':
            bot.send_message(message.from_user.id, 'Мои социальные сети', reply_markup=ekaterina_buttons.user_smm())
            bot.register_next_step_handler(message, user_check_command)
    else:
        bot.send_message(message.from_user.id, 'Введена неизвестная команда, попробуйте ещё раз', reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)


# ГЛАВНОЕ МЕНЮ - получение запроса
def user_get_request(message):
    if message.text == 'Отмена':
        bot.send_message(message.from_user.id, 'Выберите дейсвтие', reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)
    
    # дописать функционал по приёму ответов Да/нет
    else:
        yes_no = message.text
        bot.send_message(message.from_user.id, text_messages.TAKE_REQUEST_2, reply_markup=ekaterina_buttons.admin_ages())
        bot.register_next_step_handler(message, user_get_request_age, yes_no)

def user_get_request_age(message, yes_no):
    if message.text =='Отмена':
        bot.send_message(message.from_user.id, 'Регистрация на консультацию остановлена\n\nВыберите действие', reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)
    else:
        age = message.text
        bot.send_message(message.from_user.id, text=text_messages.TAKE_REQUEST_3, reply_markup=ekaterina_buttons.category())
        bot.register_next_step_handler(message, user_get_request_category, yes_no, age)

def user_get_request_category(message, yes_no, age):
    if message.text =='Отмена':
        bot.send_message(message.from_user.id, 'Регистрация на консультацию остановлена\n\nВыберите действие', reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)
    else:
        category = message.text
        bot.send_message(message.from_user.id, text=text_messages.TAKE_REQUEST_4, reply_markup=ekaterina_buttons.admin_wishes())
        bot.register_next_step_handler(message, user_get_request_wishes, yes_no, age, category)

def user_get_request_wishes(message, yes_no, age, category):
    if message.text =='Отмена':
        bot.send_message(message.from_user.id, 'Регистрация на консультацию остановлена\n\nВыберите действие', reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)
    else:
        wish = message.text
        bot.send_message(message.from_user.id, text=text_messages.TAKE_REQUEST_5, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, user_get_request_comment, yes_no, age, category, wish)

def user_get_request_comment(message, yes_no, age, category, wish):
    comment = message.text
    bot.send_message(message.from_user.id, text=text_messages.TAKE_REQUEST_6, reply_markup=ekaterina_buttons.phone())
    bot.register_next_step_handler(message, user_get_request_phone, yes_no, age, category, wish, comment)

def user_get_request_phone(message, yes_no, age, category, wish, comment):
    if message.text:

        text = message.text
        if text == 'Отмена':
            bot.send_message(message.from_user.id, 'Действие отменено', reply_markup=ekaterina_buttons.user_main())
            bot.register_next_step_handler(message, user_check_command)
        elif "+" in text:
            text_1 = text.split('+')
            phone_number = text_1[1:]
            bot.send_message(message.from_user.id, text_messages.TAKE_REQUEST_7, reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, user_get_request_name,yes_no, age, category, wish, comment, phone_number)
        else:
            phone_number = text
            bot.send_message(message.from_user.id, text_messages.TAKE_REQUEST_7, reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, user_get_request_name, yes_no, age, category, wish, comment, phone_number)

    elif message.contact.phone_number:
        phone_number =  message.contact.phone_number
        #print(message)
        bot.send_message(message.from_user.id, text_messages.TAKE_REQUEST_7, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, user_get_request_name,yes_no, age, category, wish, comment, phone_number)
    else:
        bot.send_message(message.from_user.id, 'Произошла ошибка в боте.\n\n\nДавайте попробуем еще раз', reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)

def user_get_request_name(message, yes_no, age, category, wish, comment, phone_number ):
    name = message.text
    username = message.from_user.username

    ekaterina_data.new_user_add(message.from_user.id, name, username, phone_number, category, wish, comment, yes_no, age)
    id = len(ekaterina_data.get_quantity_requests()) + 1

    bot.send_message(int(GROUP_ID),
                    text = f'''<b>Новый запрос:</b>

    <b>ID:</b> <i>{str(id)} </i>
    <b>Имя:</b> <i>{name}</i> | @{username}
    <b>Телефон:</b> {phone_number}
    <b>Сфера:</b> <i>{category}</i>
    <b>Пожелания:</b> <i>{wish}</i>
    <b>Комментарий:</b> <i>{comment}</i>

    <b>Telegram id:</b> '{message.from_user.id}'
    ''',
    parse_mode='html')

    bot.send_message(message.from_user.id, text=text_messages.TAKE_REQUEST_8, reply_markup=ekaterina_buttons.user_main())
    bot.register_next_step_handler(message, user_check_command)

# ГЛАВНОЕ МЕНЮ - получение вопроса
#def user_get_question(message):
    
  # bot.send_message(message.from_user.id, text_messages.ASK_QUESTION)
  # bot.register_next_step_handler(message, user_get_question_body)

def user_get_question_body(message):
    if message.text == 'Отмена':
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)
    else:
        text_question = message.text

        bot.send_message(message.from_user.id, text='Введите ваше имя')
        bot.register_next_step_handler(message, user_get_question_name, text_question)

def user_get_question_name(message, text_question):
    name = message.text

    if message.from_user.username:
        ekaterina_data.new_question(message.from_user.id, name, message.from_user.username, text_question)
        bot.send_message(chat_id = int(GROUP_ID), text = ekaterina_data.get_question_new_message()[0])
        bot.send_message(message.from_user.id, 'Ваш вопрос успешно отправлен\n\nВыберите следующее действие', reply_markup=ekaterina_buttons.user_main())
        bot.register_next_step_handler(message, user_check_command)
    else:
        bot.send_message(message.from_user.id, 'Введите способо связи или контактные данные одним сообщением', reply_markup=ekaterina_buttons.phone())
        bot.register_next_step_handler(message, user_get_question_contact, name, text_question)

def user_get_question_contact(message, name, text_question):
    contact = message.text

    ekaterina_data.new_question(message.from_user.id, name, contact, text_question)
    bot.send_message(int(GROUP_ID), ekaterina_data.get_question_new_message()[0])
    bot.send_message(message.from_user.id, 'Ваш вопрос успешно отправлен\n\nВыберите следующее действие', reply_markup=ekaterina_buttons.user_main())
    bot.register_next_step_handler(message, user_check_command)


# ОБРАБОТЧИК КОМАНД inline клавиатур
@bot.callback_query_handler(func= lambda call: True)
def callback_inline(call):
    '''
    Это обработчик inline-клавиатур, где сначала узнается номер таблицы по которой будет вестись поиск
    Узнаем номер таблицы и изменяем сообщение по уже новой, имеющейся информации
    '''
    data = call.data
    table = data[0]
    if table == '1':
        text = ekaterina_data.get_request_id(data[2:])
        bot.edit_message_text(
                            text = text,
                            parse_mode='html',
                            chat_id=call.from_user.id,
                            message_id=call.message.message_id, 
                            reply_markup=ekaterina_buttons.admin_get_quantity_requests_inline()
                            )
    elif table == '2':
        text = ekaterina_data.get_question_id(data[2:])
        bot.edit_message_text(
                            text = text,
                            parse_mode='html',
                            chat_id=call.from_user.id,
                            message_id=call.message.message_id,
                            reply_markup=ekaterina_buttons.admin_get_quantity_question_inline()
                            )

    if call.data == 'send_message_id_yes':
        bot.send_message(call.from_user.id, 'Отправьте Telegram_id (он указан выше)')

    if call.data == 'answer_question_id':
        bot.send_message(call.from_user.id, 'Отправьте Telegram_id (он указан выше)')

bot.polling(non_stop=True)

