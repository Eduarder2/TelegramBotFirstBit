

import telebot

class Manager(telebot.TeleBot):
    
    def __init__(self, name, id_):
        self.name = name
        self.id = id_

    def get_number_of_order(self):
        pass

    def get_clients_name(self):
        pass

    def get_phone(self):
        pass

    def get_problem(self):
        pass

    def get_scheduled_date(self):
        pass

    def send_message_to_coordinator(self):
        self.get_number_of_order()
        self.get_clients_name()
        self.get_phone()
        self.get_problem()
        self.get_scheduled_date()


        
class Implementer(telebot.TeleBot):
    pass

class Coordinator(telebot.TeleBot):
    pass

class Administrator(telebot.TeleBot):
    pass
