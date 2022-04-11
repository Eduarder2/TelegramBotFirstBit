

import telebot
from telebot import types

from order import Order

PATH_ID_POSITION_NAME = 'C:\\Users\\Эдуард\\Desktop\\1.txt'

try:
    with open('TOKEN.txt') as token:
        TOKEN = token.readline()
except FileNotFoundError:
    raise FileNotFoundError('A token of bot not found.')

# Почти во все методы необходимо добавить кнопку "Назад", возможно, 
# стоит сделать это глобальной фунцией или методом суперкласса ActiveUser

class ActiveUser(telebot.TeleBot):

    def __init__(self, name, id_, token=TOKEN):
        super().__init__(token)
        self.name = name
        self.id = id_
        self.state_order = 1

        back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, 
                                                  one_time_keyboard=True)
        but_back = types.KeyboardButton('Назад')
        back_keyboard.add(but_back)
        self.back_keyboard = back_keyboard

    #def undo_last_action(self):
    #    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #    button_undo = types.KeyboardButton('Назад')
    #    markup.add(button_undo)



class Manager(ActiveUser):
    
    def __init__(self, name, id_, id_coordinator='935171424'):
        super().__init__(name, id_)
        self.id_coordinator = id_coordinator
        self.message_to_coordinator = {
            # 1 - номер наряда, 2 - имя клиента, 3 - телефон клиента,
            # 4 - описание проблемы клиента, 5 - срок исполнения,
            # 0 - имя менеджера,
            
            # Стоит привести словарь к виду {number: [value, field_name]}
            # Для большей читаемости
           
            'state': 1,
            0: self.name,
            1: '',
            2: '',
            3: '',
            4: '',
            5: '',
            }

    def change_message_to_coordinator(self, message):
        state = self.message_to_coordinator['state']
        self.message_to_coordinator[state] = message.text
        self.message_to_coordinator['state'] += 1
        

    def get_number_of_order(self, message):
        super().send_message(self.id, 'Введите номер наряда')
        self.change_message_to_coordinator(message)


    def get_clients_name(self, message):
        super().send_message(self.id, 'Введите имя клиента')
        self.change_message_to_coordinator(message)


    def get_phone(self, message):
        super().send_message(self.id, 'Введите номер телефона, по '
                             'которому нужно позвонить внедренцу')
        self.change_message_to_coordinator(message)


    def get_problem(self, message):
        super().send_message(self.id, 'Кратко опишите снятую задачу')
        self.change_message_to_coordinator(message)


    def get_scheduled_date(self, message):
        super().send_message(self.id, 'Введите сроки исполнения, '
                             'согласованные с клиентом, либо напишите - '
                             ' нет - если четкие сроки не обсуждались')
        self.change_message_to_coordinator(message)


    def send_message_to_coordinator(self):
        self.message_to_coordinator['state'] = 1
        super().send_message(self.id_coordinator,
                             text=str(self.message_to_coordinator))

    
    def dialog_with_bot(self, message):
        state = self.message_to_coordinator['state']
        if state == 1:
            self.get_number_of_order(message)
        elif state == 2:
            self.get_clients_name(message)
        elif state == 3:
            self.get_phone(message)
        elif state == 4:
            self.get_problem(message)
        elif state == 5:
            self.get_scheduled_date(message)
        elif state == 6:
            self.send_message_to_coordinator()

        
class Implementer(telebot.TeleBot):
    
    def __init__(self):
        pass


    def give_list_of_orders(self):
        pass


    def get_date_start_fact(self):
        pass


    def get_date_finish(self):
        pass


    def send_message_to_manager(self):
        pass


    def send_message_to_coordinator(self):
        pass


    def dialog_with_bot(self, message):
        pass


class Coordinator(ActiveUser):
    
    def __init__(self, name, id_):
        '''Закончена
        '''
        super().__init__(name, id_)
        self.state = ['Главное меню', None, None]

        main_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, 
                                row_width=2)
        but_upper_left = types.KeyboardButton('Распределить наряд')
        but_upper_right = types.KeyboardButton('Списки нарядов')
        but_lower_left = types.KeyboardButton('Список сотрудников')
        but_lower_right = types.KeyboardButton('Список активных'
                                               ' пользователей')
        main_keyboard.add(but_upper_left, but_upper_right, 
                          but_lower_left, but_lower_right)
        self.main_keyboard = main_keyboard

        lists_of_orders_keyboard = types.ReplyKeyboardMarkup(
                                        one_time_keyboard=True, row_width=2)
        but_upper_left = types.KeyboardButton('Активные наряды внедренцев')
        but_upper_right = types.KeyboardButton('Наряды, распределенные на '
                                               'внедренцев')
        but_lower_left = types.KeyboardButton('Наряды, распределенные на '
                                              'координатора')
        but_lower_right = types.KeyboardButton('Назад')
        lists_of_orders_keyboard.add(but_upper_left, but_upper_right, 
                                     but_lower_left, but_lower_right)
        self.lists_of_orders_keyboard = lists_of_orders_keyboard

        list_of_employees_keyboard = types.ReplyKeyboardMarkup(
                                        one_time_keyboard=True, row_width=2)
        but_upper_left = types.KeyboardButton('Добавить сотрудника')
        but_upper_right = types.KeyboardButton('Удалить сотрудника')
        but_lower = types.KeyboardButton('Назад')
        list_of_employees_keyboard.add(but_upper_left, but_upper_right, 
                                       but_lower)
        self.list_of_employees_keyboard = list_of_employees_keyboard
        

    def give_main_menu(self, error=False):
        '''Закончена
        '''
        self.state = ['Главное меню', 0, 0]
        if error:
            super().send_message(self.id, 'Не понял вас! Повторите попытку,'
                                 ' используя всплывающую клавиатуру.', 
                                 reply_markup=self.main_keyboard)
        else:
            super().send_message(self.id, 'Главное меню',
                                 reply_markup=self.main_keyboard)


    def give_orders_menu(self, error=False):
        '''Закончена
        '''
        self.state[0] = 'Списки нарядов'
        if error:
            super().send_message(self.id, 'Не понял вас! Повторите попытку,'
                                 ' используя всплывающую клавиатуру.', 
                                 reply_markup=self.lists_of_orders_keyboard)
        else:
            super().send_message(self.id, 'Какой список вы хотите получить?',
                                 reply_markup=self.lists_of_orders_keyboard)


    def give_employees_menu(self, error=False):
        '''Закончена
        '''
        self.state[0] = 'Список сотрудников'
        if error:
            super().send_message(self.id, 'Не понял вас! Повторите попытку,'
                                 ' используя всплывающую клавиатуру.', 
                                 reply_markup=self.list_of_employees_keyboard)
        else:
            super().send_message(self.id, 'Зарегистрированные мной '
                    'сотрудники. Вы можете добавить или удалить некоторых:',
                    reply_markup=self.list_of_employees_keyboard)


    def give_list_of_orders(self, kind):
        ''' Не закончена, надо знать как и где хранится БД с нарядами.
        Также надо определить класс Order.
        '''
        if kind == 'Активные наряды внедренцев':
            pass
        elif kind == 'Наряды, распределенные на внедренцев':
            pass
        elif kind == 'Наряды, распределенные на координатора':
            super().send_message(self.id, 'Эти наряды вам следует '
                                 'распределить на внедренцев:')
            pass
        else:
            self.give_orders_menu(error=True)
            return
        self.give_main_menu()

    def give_list_of_active_users(self):
        super().send_message(self.id, 'Сегодня со мной уже связались:',
                             reply_markup=self.main_keyboard)


    def give_list_of_employees(self):
        pass


    def add_employee(self, id_employee, position_employee, name_employee):
        with open(PATH_ID_POSITION_NAME, 'a', encoding='UTF-8') as employees:
            employees.write(id_employee + '\t' + position_employee +
                            '\t' + name_employee)
        super().send_message(self.id, 'Изменения вступят в силу при следующем'
                             ' запуске бота!')


    def delete_employee(self, id_):
        # Необходимо осуществить проверку в БД (НЕ в архиве), 
        # есть ли активные наряды, связанные с этим сотрудником.

        with open(PATH_ID_POSITION_NAME, encoding='UTF-8') as employees:
            list_ = employees.readlines()
        for i in range(len(list_) - 1, -1, -1):
            if list_[i].find(id_) != -1:
                list_.pop(i)
        with open(PATH_ID_POSITION_NAME, 'wt', encoding='UTF-8') as employees:
            employees.writelines(list_)
        super().send_message(self.id, 'Изменения вступят в силу при следующем'
                             ' запуске бота!')

    
    def get_number_of_order(self, message):
        pass
    

    def get_implementer(self, message):
        pass


    def get_date_start_plan(self, message):
        pass


    def send_message_to_implementer(self, message):
        if self.state[1] == 0:
            self.state[0] = 'Распределить наряд'
            self.give_list_of_orders(kind='Наряды, распределенные на '
                                     'координатора')
            self.get_number_of_order(message)
        elif self.state[1] == 1:
            self.get_implementer(message)
        elif self.state[1] == 2:
            self.get_date_start_plan(message)
        elif self.state[1] == 3:
            # Здесь будет отправка сообщения внедренцу
            self.state[1] = -1
            pass
        self.state[1] += 1



    def dialog_with_bot(self, message):

        if self.state[0] == 'Главное меню':
            if message.text == 'Приступим':
                self.give_main_menu()
            elif message.text == 'Список активных пользователей':
                self.give_list_of_active_users()
            elif message.text == 'Список сотрудников':
                self.give_employees_menu()
            elif message.text == 'Списки нарядов':
                self.give_orders_menu()
            elif message.text == 'Распределить наряд':
                self.send_message_to_implementer(message)
            else:
                self.give_main_menu(error=True)
        elif self.state[0] == 'Список сотрудников':
            if self.state[1] == 'Добавить сотрудника':
                self.add_employee(message)
            elif self.state[1] == 'Удалить сотрудника':
                self.delete_employee(message)
            elif message.text in {'Добавить сотрудника', 'Удалить сотрудника'}:
                self.give_list_of_employees()
                self.state[1] = message.text
            elif message.text == 'Назад':
                self.give_main_menu()
            else:
                self.give_employees_menu(error=True)          
        elif self.state[0] == 'Списки нарядов':
            if message.text == 'Назад':
                self.give_main_menu()
            else:
                self.give_list_of_orders(kind=message.text)
        elif self.state[0] == 'Распределить наряд':
            if message.text == 'Назад':
                self.give_main_menu()
            else:
                self.send_message_to_implementer(message)
        else:
            self.give_main_menu(error=True)





class Administrator(Coordinator):
    
    def __init__(self, name, id_):
        super().__init__(name, id_)


    def change_coordinator(self, id_old_coordinator, id_new_coordinator, name_employee):
        ''' Функция для замены координатора.

        Эквивалентна вызову двух функций: 
        Coordinator.delete_employee(id_old_coordinator)
        Coordinator.add_employee(id_new_coordinator, 'coordinator', name_employee)
        Используется, если старый координатор не добавил нового,
        но себя уже удалил
        
        '''
        super().delete_employee(id_old_coordinator)
        super().add_employee(id_new_coordinator, 'coordinator', name_employee)


    def dialog_with_bot(self, message):
        pass

