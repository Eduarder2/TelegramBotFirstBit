

import telebot
import positions

# Username пользователей, взаимодействующих с ботом
active_users = {
    'manager': [],
    'implementer': [],
    'coordinator': [],
    'administrator': []
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

        # Необходимо добавить кнопку "Приступим!"
        

        # Создаем экземпляр класса, соответствующего должности 
        # И переходим к обработке наряда при нажатии кнопки "Приступим!"
        bot.send_message(id_, 'Привет, ' + id_position_name[id_][1])
        pos = id_position_name[id_][0]
        name = id_position_name[id_][1]
        if pos == 'manager':
            active_users[pos].append({id_: positions.Manager(name, id_)})
        elif pos == 'implementer':
            active_users[pos].append({id_: positions.Implementer(name, id_)})
        elif pos == 'coordinator':
            active_users[pos].append({id_: positions.Coordinator(name, id_)})
        elif pos == 'administrator':
            active_users[pos].append({id_: positions.Administrator(name, id_)})
        else:
            pass # Написать обработку исключений

    
@bot.message_handler(content_types=['text'])
def process_order(message):
    id_ = str(message.chat.id)
    pos = id_position_name[id_][0]
    if pos == 'manager':
        if message.text == 'Приступим!':
            # Возможно исключение - KeyError - если экземпляр класса 
            # еще не создан. Ошибка возникнет при отправке сообщения 
            # "Приступим!", без команды /start

            active_users[pos][id_].send_message_to_coordinator()
    elif pos == 'implementer':
        pass
    elif pos == 'coordinator':
        pass
    elif pos == 'administrator':
        pass
    else:
        pass 




bot.infinity_polling()