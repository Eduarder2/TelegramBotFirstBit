

import telebot
from telebot import types

# Почти во все методы необходимо добавить кнопку "Назад", возможно, 
# стоит сделать это глобальной фунцией или методом суперкласса ActiveUser

class Manager(telebot.TeleBot):

    
    def __init__(self, name, id_, id_coordinator='935171424'):
        self.name = name
        self.id = id_
        self.id_coordinator = id_coordinator
        self.message_to_coordinator = {
            # 1 - номер наряда, 2 - имя клиента, 3 - телефон клиента,
            # 4 - описание проблемы клиента, 5 - срок исполнения,
            # 6 - имя менеджера,
            
            # Стоит привести словарь к виду {number: [value, field_name]}
            # Для большей читаемости
           
            'state': 1,
            1: '',
            2: '',
            3: '',
            4: '',
            6: self.name,
            }

    def change_message_to_coordinator(self, message):
        state = self.message_to_coordinator['state']
        self.message_to_coordinator[state] = message.text
        self.message_to_coordinator['state'] += 1
        

    def get_number_of_order(self, message):
        super().send_message(self.id, text='Введите номер наряда')
        self.change_message_to_coordinator(self, message)


    def get_clients_name(self, message):
        super().send_message(self.id, text='Введите имя клиента')
        self.change_message_to_coordinator(self, message)


    def get_phone(self, message):
        super().send_message(self.id, text='Введите номер телефона, по ' +\
                             'которому нужно позвонить внедренцу')
        self.change_message_to_coordinator(self, message)


    def get_problem(self, message):
        super().send_message(self.id, 'Кратко опишите снятую задачу')
        self.change_message_to_coordinator(self, message)


    def get_scheduled_date(self, message):
        super().send_message(self.id, 'Введите сроки исполнения, ' +\
                             'согласованные с клиентом, либо напишите - ' +\
                             ' нет - если четкие сроки не обсуждались')
        self.change_message_to_coordinator(self, message)


    def send_message_to_coordinator(self):
        self.message_to_coordinator['state'] = 1
        super().send_message(self.id_coordinator,\
                             text=str(self.message_to_coordinator))


        
class Implementer(telebot.TeleBot):
    pass

class Coordinator(telebot.TeleBot):
    pass

class Administrator(telebot.TeleBot):
    pass
