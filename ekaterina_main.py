import telebot
from telebot import types

import ekaterina_buttons
import ekaterina_data
from config import TOKEN

import datetime
import time
import pytz



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
                            reply_markup=ekaterina_buttons.admin_send_message()
                            )
            bot.register_next_step_handler(message, admin_send_message)

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
            time.sleep(0.5)
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
    bot.send_message(message.from_user.id, data[1], reply_markup=ekaterina_buttons.admin_send_message(), parse_mode='html')
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
        bot.send_message(message.from_user.id, data[0], reply_markup=ekaterina_buttons.admin_send_message())
        bot.register_next_step_handler(message, admin_request_username_action, data)
    else:
        data = ekaterina_data.get_request_username(username)
        bot.send_message(message.from_user.id, data[0], reply_markup=ekaterina_buttons.admin_send_message())
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
            pass
        elif command == 'Получить вопрос по имени':
            pass
        elif command == 'Получить вопрос по username':
            pass
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


    '''
    ДОПИСАТЬ ФУНКЦИОНАЛ ДЛЯ РАБОТЫ С ВОПРОСАМИ
    '''

#---#---#---#---#---#---#---#---#---
#---#---#---#---#---#---#---#---#---#---#---#---
#---#---#---#---#---#---#---#---#---#---#---#---

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
        message = ekaterina_data.get_request_id(data[2:])
        bot.edit_message_text(
                            text = message,
                            parse_mode='html',
                            chat_id=call.from_user.id,
                            message_id=call.message.message_id, 
                            reply_markup=ekaterina_buttons.admin_get_quantity_requests_inline()
                            )
    if call.data == 'send_message_id_yes':
        bot.send_message(call.from_user.id, 'Отправьте Telegram_id (он указан выше)')


bot.polling(non_stop=True)