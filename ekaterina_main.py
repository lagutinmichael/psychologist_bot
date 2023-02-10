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
                            reply_markup=ekaterina_buttons.admin_get_quantity_requests_inline()
                            )
            bot.register_next_step_handler(message, admin_requests_menu)

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
    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, попробуйте другую или можете вернуться в главное меню', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_requests_menu)

# ГЛАВНОЕ МЕНЮ - ЗАПРОСЫ - по иммени
def admin_request_name(message):
    name = message.text
    data = ekaterina_data.get_request_name(name)
    bot.send_message(message.from_user.id, data[0], reply_markup=ekaterina_buttons.admin_send_message())
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
    data = ekaterina_data.get_request_username(username)

    if username[0] == '@':
        bot.send_message(message.from_user.id, data[0], reply_markup=ekaterina_buttons.admin_send_message())
        bot.register_next_step_handler(message, admin_request_username_action, data)
    else:
        username = '@'+username
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
def admin_request_id_action(message, data):
    command = message.text

    if command == 'Отправить сообщение':
        bot.send_message(message.from_user.id, 'Отправьте сообщение пользователю', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_request_id_action_message, data)
    elif command == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите действие с запросами', reply_markup=ekaterina_buttons.admin_get_requests())
        bot.register_next_step_handler(message, admin_requests_menu)
    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, начните с начала', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)

def admin_request_id_action_message(message, data):
    text = message.text

    bot.send_message(data[1], text)
    bot.send_message(message.from_user.id, 'Сообщение успешно доставлено пользователю \nВыберите действие', reply_markup=ekaterina_buttons.admin_main())
    bot.register_next_step_handler(message, admin_check_command)



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
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id, 
                            reply_markup=ekaterina_buttons.admin_get_quantity_requests_inline(),
                            )
        #bot.register_next_step_handler(call, admin_request_id_action)


bot.polling(non_stop=True)