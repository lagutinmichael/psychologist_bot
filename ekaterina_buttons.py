from telebot import types
import ekaterina_data


# USER основные кнопки
def user_main():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    bt1 = types.KeyboardButton('Записаться на консультацию')
    bt2 = types.KeyboardButton('Задать вопрос')
    bt3 = types.KeyboardButton('Обо мне')
    bt4 = types.KeyboardButton('Мои соц.сети')

    kb.add(bt1, bt2, bt3, bt4)
    
    return kb

# USER социальные сети
def user_smm():
    kb = types.InlineKeyboardMarkup(row_width=2)

    bt1 = types.InlineKeyboardButton('Instagram', url='https://www.instagram.com/saburova_k_/')
    bt2 = types.InlineKeyboardButton('Facebook', url='')
    bt3 = types.InlineKeyboardButton('Telegram', url='https://t.me/Saburova_Katerina_psy')

    kb.add(bt1, bt2, bt3)

    return kb

# USER да/нет
def user_yes_no():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    bt1 = types.KeyboardButton('Да')
    bt2 = types.KeyboardButton('Нет')
    bt3 = types.KeyboardButton('Отмена')

    kb.add(bt1, bt2, bt3)
    
    return kb



# USER кнопка номера телефона
def phone():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Отправить контакт', request_contact=True)
    button_2 = types.KeyboardButton('Отмена')

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

    list_buttons = [types.KeyboardButton(i) for i in data]
   # for i in data:
   #     kb.add(types.KeyboardButton(i))
    kb.add(list_buttons)
    return kb

def admin_wishes():
    data = ekaterina_data.get_list_wishes()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

    #list_buttons = [types.KeyboardButton(i) for i in data]
    #kb.add(list_buttons)
    for i in data:
        kb.add(types.KeyboardButton(i))
    kb.row(types.KeyboardButton('Отмена'))
    return kb

# ВОЗРАСТ
def admin_ages():
    data = ekaterina_data.get_list_age()

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

    for i in data:
        kb.add(types.KeyboardButton(i))

    kb.row(types.KeyboardButton('Отмена'))
    return kb

# USER кнопки с категориями
def category():
    data = ekaterina_data.get_list_category()

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    for i in data:
        kb.add(types.KeyboardButton(i))

    kb.add(types.KeyboardButton('Отмена'))
    return kb

# ADMIN кнопки со статусами 
def admin_category():
    data = ekaterina_data.admin_get_status()

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    for i in data:
        kb.add(types.KeyboardButton(i))

    kb.add(types.KeyboardButton('Отмена'))
    return kb



## ADMIN BUTTONS

# ADMIN кнопки на главной странице
def admin_main():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Запросы')
    button_2 = types.KeyboardButton('Вопросы')
    button_3 = types.KeyboardButton('Статистика')
    button_4 = types.KeyboardButton('Рассылка')
    #button_5 = types.KeyboardButton('Работа с клиентом')
    # не помню функционал кнопки

    kb.add(button_1, button_2, button_3, button_4)

    return kb

# ADMIN отправка сообщения, после поиска нужного человека
def admin_send_message():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)

    button_1 = types.KeyboardButton('Отправить сообщение')
    button_2 = types.KeyboardButton('Назад') 

    kb.add(button_1, button_2)

    return kb

# ADMIN кнопки работы с вопросами
def admin_get_question():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Получить вопрос по ID')
    button_2 = types.KeyboardButton('Получить вопрос по имени')
    button_3 = types.KeyboardButton('Получить вопрос по username')
    button_4 = types.KeyboardButton('Назад')

    kb.add(button_1, button_2, button_3, button_4)

    return kb

# ADMIN кнопки работы со статистикой
def admin_get_statistics():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Количество заявок')
    button_2 = types.KeyboardButton('Количество пользователей')
    button_3 = types.KeyboardButton('Назад')

    kb.add(button_1, button_2, button_3)

    return kb

# ADMIN кнопки по выгрузке информации из базы
def admin_get_requests():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Получить запрос по ID')
    button_2 = types.KeyboardButton('Получить запрос по имени')
    button_3 = types.KeyboardButton('Получить запрос по username')
    #button_4 = types.KeyboardButton('Получить запрос по статусу')
    #button_5 = types.KeyboardButton('Получить запрос по сфере/категории')
    button_6 = types.KeyboardButton('Назад')


    kb.add(button_1, button_2, button_3, button_6)

    return kb


# InlineKeybord для выбора номера запроса по ID
def admin_get_quantity_requests_inline():
    data = ekaterina_data.get_quantity_requests()
    a = len(data) # количество элементов в таблице
    c = a%5 # остаток от деления на 5
    if c == 0:
        b = (a//5) # количество строк для кнопок
    else:
        b = (a//5) + 1 # колличество строк, если в последней строке не все кнопки
    
    kb = types.InlineKeyboardMarkup(row_width=5)
    index = 0
    for i in range(b):
        bt1 = types.InlineKeyboardButton(str(1+index), callback_data='1_'+f'{1+index}')
        bt2 = types.InlineKeyboardButton(str(2+index), callback_data='1_'+f'{2+index}')
        bt3 = types.InlineKeyboardButton(str(3+index), callback_data='1_'+f'{3+index}')
        bt4 = types.InlineKeyboardButton(str(4+index), callback_data='1_'+f'{4+index}')
        bt5 = types.InlineKeyboardButton(str(5+index), callback_data='1_'+f'{5+index}')

        kb.row(bt1, bt2, bt3, bt4, bt5)
        
        index +=5

    return kb

# InlineKeybord для выбора номера вопроса по ID
def admin_get_quantity_question_inline():
    data = ekaterina_data.get_quantity_questions()
    a = len(data) # количество элементов в таблице
    c = a%5 # остаток от деления на 5
    if c == 0:
        b = (a//5) # количество строк для кнопок
    else:
        b = (a//5) + 1 # колличество строк, если в последней строке не все кнопки
    
    kb = types.InlineKeyboardMarkup(row_width=5)
    index = 0
    for i in range(b):
        bt1 = types.InlineKeyboardButton(str(1+index), callback_data='2_'+f'{1+index}')
        bt2 = types.InlineKeyboardButton(str(2+index), callback_data='2_'+f'{2+index}')
        bt3 = types.InlineKeyboardButton(str(3+index), callback_data='2_'+f'{3+index}')
        bt4 = types.InlineKeyboardButton(str(4+index), callback_data='2_'+f'{4+index}')
        bt5 = types.InlineKeyboardButton(str(5+index), callback_data='2_'+f'{5+index}')

        kb.row(bt1, bt2, bt3, bt4, bt5)
        
        index +=5

    return kb


# InlineKeybord для ответа на запрос
def admin_send_message_inline():
    kb = types.InlineKeyboardMarkup()
    
    bt1 = types.InlineKeyboardButton('Да', callback_data='send_message_id_yes')
    #bt2 = types.InlineKeyboardButton('Нет', callback_data='send_message_id_no')

    kb.add(bt1)

    return kb

# InlineKeyboard для ответа на сообщения
def admin_answer_question_inline():
    kb = types.InlineKeyboardMarkup()

    bt = types.InlineKeyboardButton('Да', callback_data='answer_question_id')

    kb.add(bt)

    return kb


# клавиатура выбора куда отправлять рассылку
def admin_mailng_main():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

    bt1 = types.KeyboardButton('Категории/Сфера')
    #bt2 = types.KeyboardButton('Пожелания')
    #bt3 = types.KeyboardButton('Статус')
    bt4 = types.KeyboardButton('Всем')
    bt5 = types.KeyboardButton('Назад')

    kb.add(bt4, bt1)
    kb.row(bt5)

    return kb

# INLINE клавиатура с кнопками социальных сетей
def user_smm():
    kb = types.InlineKeyboardMarkup()

    bt1 = types.InlineKeyboardButton('Instagram', url='https://www.instagram.com/saburova_k_/')
    bt2 = types.InlineKeyboardButton('Facebook', url='https://www.instagram.com/saburova_k_/')

    kb.add(bt1, bt2)

    return kb
