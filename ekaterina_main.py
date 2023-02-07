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

def admin_check_command(message):
    command = message.text
    command_list = ['Запросы', 'Вопросы', 'Статистика', 'Рассылка']
    if command in command_list:
        if command == command_list[0]:
            bot.send_message(message.from_user.id, 'Выберите действие с Запросами', reply_markup=ekaterina_buttons.admin_get_requests())
            bot.register_next_step_handler(message, admin_requests_menu)
        elif command == command_list[1]:
            bot.send_message(message.from_user.id, 'Выберите действие с Вопросами', reply_markup=ekaterina_buttons.admin_get_question())
            bot.register_next_step_handler(message, admin_question_menu)
        elif command == command_list[2]:
            bot.send_message(message.from_user.id, 'Какую статистику вы хотите узнать?', reply_markup=ekaterina_buttons.admin_get_statistics())
            bot.register_next_step_handler(message, admin_statistics_menu)
        elif command == command_list[3]:
            bot.send_message(message.from_user.id, 'Выберите, кому хотите отрпавить рассылку', reply_markup=ekaterina_buttons.admin_send_message())
            bot.register_next_step_handler(message, admin_send_message)
        else:
            bot.send_message(message.from_user.id, 'Команда не найдена. \nПопробуйте еще раз или свяжитесь с разработчиком бота')
            bot.register_next_step_handler(message, admin_check_command)
    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, попробуйте другую', reply_markup=ekaterina_buttons.admin_main())
        bot.register_next_step_handler(message, admin_check_command)

def admin_requests_menu(message):
    command = message.text
    command_list = ['Получить запрос по ID', 'Получить запрос по имени', 'Получить запрос по username', 'Получить запрос по статусу', 'Получить запрос по сфере/категории', 'Назад', 'Отмена']

    if command in command_list:
        if command == 'Получить запрос по ID':
            bot.send_message(message.from_user.id, 'Введите/выберите ID (номер) запроса', reply_markup=ekaterina_buttons.admin_get_quantity_requests())
    else:
        bot.send_message(message.from_user.id, 'Команда не распознана, попробуйте другую или можете вернуться в главное меню', reply_markup=ekaterina_buttons.cancel())
        bot.register_next_step_handler(message, admin_requests_menu)


bot.polling(non_stop=True)