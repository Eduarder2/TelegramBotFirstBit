

import telebot
from telebot import types

import positions
from positions import PATH_ID_POSITION_NAME

# Username пользователей, взаимодействующих с ботом
active_users = {
    'manager': dict(),
    'implementer': dict(),
    'coordinator': dict(),
    'administrator': dict()
    }


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
    ''' Функция начала рабочего дня. Выполняется при использовании 
    команды /start в диалоге с ботом.
    
    Аргумент - message (см. https://core.telegram.org/bots/api), 
    message.text всегда равен str(/start). Функция всегда возвращает 
    некоторое сообщение любому пользователю, а если пользователь 
    сотрудник компании, то создает экземпляр класса, соответствующего 
    должности (positions) и вызывает функцию process_order
    
    '''

    id_ = str(message.chat.id)
    if not id_ in id_position_name:
        bot.send_message(id_, text='Вы не числитесь сотрудником компании. '
                         'Для уточнения информации обратитесь к координатору.')
    else:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        button_ready = types.KeyboardButton('Приступим!')
        markup.add(button_ready)

        bot.send_message(id_, 'Привет, ' + id_position_name[id_][1],
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
    ''' Функция вызывается при отправки любого текстового сообщения 
    боту, отличного от команд типа /start.

    Аргумент - message (см. https://core.telegram.org/bots/api). 
    Функция осуществляет взаимодействие с сотрудником в зависимости 
    от его должности (см. positions). Если пользователь не сотрудник, 
    то он получит соответствующее сообщение. 

    '''
    id_ = str(message.chat.id)
    if id_ in id_position_name:
        pos = id_position_name[id_][0]
        if id_ in active_users[pos]:
            active_users[pos][id_].dialog_with_bot(message)
        else:
            bot.send_message(id_, text='Рабочий день стоит начинать'
                             ' с команды /start')
    else:
        bot.send_message(id_, text='Вы не числитесь сотрудником компании. '
                         'Для уточнения информации обратитесь к координатору.')


bot.infinity_polling()