

import telebot
from telebot import types

import positions

# Username пользователей, взаимодействующих с ботом
active_users = {
    'manager': dict(),
    'implementer': dict(),
    'coordinator': dict(),
    'administrator': dict()
    }

# Нужно определиться, где будем хранить БД
PATH_ID_POSITION_NAME = 'C:\\Users\\Эдуард\\Desktop\\1.txt'

try:
    with open('TOKEN.txt') as token:
        TOKEN = token.readline()
except FileNotFoundError:
    raise FileNotFoundError('A token of bot not found.')

try:
    with open(PATH_ID_POSITION_NAME, encoding='UTF-8') as employees:
        id_position_name = dict()
        for emp in employees:
            lst = emp.split('\t')
            id_position_name[lst[0]] = tuple(lst[1:])
except FileNotFoundError:
    with open(PATH_ID_POSITION_NAME, 'wt') as employees:
        pass


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def def_position(message):
    ''' Define position of employee (manager, admin, ...) '''

    id_ = str(message.chat.id)
    if not id_ in id_position_name.keys():
        bot.send_message(id_, text='Вы не числитесь сотрудником компании. ' +\
                         'Для уточнения информации обратитесь к координатору.')
    else:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,\
                                           one_time_keyboard=True)
        button_ready = types.KeyboardButton('Приступим!')
        markup.add(button_ready)

        # Создаем экземпляр класса, соответствующего должности 
        # И переходим к обработке наряда при нажатии кнопки "Приступим!"
        bot.send_message(id_, 'Привет, ' + id_position_name[id_][1],\
                         reply_markup=markup)
        pos = id_position_name[id_][0]
        name = id_position_name[id_][1]
        if pos == 'manager':
            active_users[pos][id_] = positions.Manager(name, id_)
        elif pos == 'implementer':
            active_users[pos][id_] = positions.Implementer(name, id_)
        elif pos == 'coordinator':
            active_users[pos][id_] = positions.Coordinator(name, id_)
        elif pos == 'administrator':
            active_users[pos][id_] = positions.Administrator(name, id_)
        else:
            pass # Написать обработку исключений

    
@bot.message_handler(content_types=['text'])
def process_order(message):
    id_ = str(message.chat.id)
    pos = id_position_name[id_][0]
    if pos == 'manager':
        if id_ in active_users[pos]:
            active_users[pos][id_].dialog_with_bot(message)
        else:
            bot.send_message(id_, text='Рабочий день стоит начинать'+\
                             ' с команды /start')
    elif pos == 'implementer':
        pass
    elif pos == 'coordinator':
        pass
    elif pos == 'administrator':
        pass
    else:
        pass 




bot.infinity_polling()