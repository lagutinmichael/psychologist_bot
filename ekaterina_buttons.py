from telebot import types
import ekaterina_data


# USER кнопка номера телефона
def phone():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Отправить контакт', request_contact=True)
    button_2 = types.KeyboardButton('Назад')

    kb.row(button_1)
    kb.row(button_2)
    return kb

# USER кнопка отмены
def cancel():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Отмена')
    kb.add(button_1)

    return kb

# USER кнопки пожеланий
def wishes():
    data = ekaterina_data.get_list_wishes()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

    for i in data:
        kb.add(types.KeyboardButton(i))

    return kb

# USER кнопки возрастов
def ages():
    data = ekaterina_data.get_list_age()

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

    for i in data:
        kb.add(types.KeyboardButton(i))

    return kb

# USER кнопки с категориями
def category():
    data = ekaterina_data.get_list_category()

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    for i in data:
        kb.add(types.KeyboardButton(i))

    return kb




## ADMIN BUTTONS

# ADMIN кнопки на главной странице
def main():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Запросы')
    button_2 = types.KeyboardButton('Вопросы')
    button_3 = types.KeyboardButton('Статистика')
    button_4 = types.KeyboardButton('Рассылка')
    #button_5 = types.KeyboardButton('Работа с клиентом')
    # не помню функционал кнопки

    kb.add(button_1, button_2, button_3, button_4)

    return kb

# ADMIN работа с пользователем (не помню функционал)
def send_message():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)

    button_1 = types.KeyboardButton('Отправить сообщение')
    button_2 = types.KeyboardButton('Назад') 

    kb.add(button_1, button_2)

    return kb

# ADMIN кнопки работы с вопросами
def get_question():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Получить вопрос по ID')
    button_2 = types.KeyboardButton('Получить вопрос по имени')
    button_3 = types.KeyboardButton('Получить вопрос по username')
    button_4 = types.KeyboardButton('Назад')

    kb.add(button_1, button_2, button_3, button_4)

    return kb

# ADMIN кнопки работы со статистикой
def get_statistics():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Колличество заявок')
    button_2 = types.KeyboardButton('Колличество пользователей')
    button_3 = types.KeyboardButton('Назад')

    kb.add(button_1, button_2, button_3)

    return kb

# ADMIN кнопки по выгрузке информации из базы
def get_info():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Получить запрос по ID')
    button_2 = types.KeyboardButton('Получить запрос по имени')
    button_3 = types.KeyboardButton('Получить запрос по username')
    button_4 = types.KeyboardButton('Получить запрос по статусу')
    button_5 = types.KeyboardButton('Получить запрос по сфере/категории')
    button_6 = types.KeyboardButton('Назад')


    kb.add(button_1, button_2, button_3, button_4, button_5, button_6)

    return kb


