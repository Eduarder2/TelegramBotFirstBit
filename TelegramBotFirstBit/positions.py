

import telebot
from telebot import types

from order import Order

PATH_ID_POSITION_NAME = 'C:\\Users\\Эдуард\\Desktop\\1.txt'

active_users = {
    'manager': dict(),
    'implementer': dict(),
    'coordinator': dict(),
    'administrator': dict()
    }

new_user = set()

try:
    with open('TOKEN.txt') as token:
        TOKEN = token.readline()
except FileNotFoundError:
    raise FileNotFoundError('A token of bot not found.')



class ActiveUser(telebot.TeleBot):

    def __init__(self, name, id_, token=TOKEN):
        super().__init__(token)
        self.name = name
        self.id = id_
        self.state_order = 1

        back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but_back = types.KeyboardButton('Назад')
        back_keyboard.add(but_back)
        self.back_keyboard = back_keyboard

        continue_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but_continue = types.KeyboardButton('Продолжить')
        continue_keyboard.add(but_continue)
        self.continue_keyboard = continue_keyboard


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

    state = ['Главное меню', 0, 0]
    stack = [state.copy()]
    
    def __init__(self, name, id_):
        super().__init__(name, id_)
        self.state = ['Главное меню', 0, 0]
        self.stack = [self.state.copy()]

        main_keyboard = types.ReplyKeyboardMarkup(row_width=2)
        but_upper_left = types.KeyboardButton('Распределить наряд')
        but_upper_right = types.KeyboardButton('Списки нарядов')
        but_lower_left = types.KeyboardButton('Список сотрудников')
        but_lower_right = types.KeyboardButton('Активные пользователи')
        main_keyboard.add(but_upper_left, but_upper_right, 
                          but_lower_left, but_lower_right)
        self.main_keyboard = main_keyboard

        lists_of_orders_keyboard = types.ReplyKeyboardMarkup(row_width=2)
        but_upper_left = types.KeyboardButton('Активные наряды внедренцев')
        but_upper_right = types.KeyboardButton('Наряды внедренцев')
        but_lower_left = types.KeyboardButton('Наряды координатора')
        but_lower_right = types.KeyboardButton('Назад')
        lists_of_orders_keyboard.add(but_upper_left, but_upper_right, 
                                     but_lower_left, but_lower_right)
        self.lists_of_orders_keyboard = lists_of_orders_keyboard

        list_of_employees_keyboard = types.ReplyKeyboardMarkup(row_width=2)
        but_upper_left = types.KeyboardButton('Добавить сотрудника')
        but_upper_right = types.KeyboardButton('Удалить сотрудника')
        but_lower = types.KeyboardButton('Назад')
        list_of_employees_keyboard.add(but_upper_left, but_upper_right, 
                                       but_lower)
        self.list_of_employees_keyboard = list_of_employees_keyboard

        position_keyboard = types.ReplyKeyboardMarkup(row_width=2)
        but_upper_left = types.KeyboardButton('manager')
        but_upper_right = types.KeyboardButton('coordinator')
        but_lower_left = types.KeyboardButton('implementer')
        but_lower_right = types.KeyboardButton('Назад')
        position_keyboard.add(but_upper_left, but_upper_right, 
                              but_lower_left, but_lower_right)
        self.position_keyboard = position_keyboard
        

    def give_main_menu(self, error=False):
        '''Возращает сообщение координатору и клавиатуру с выбором 
        функции из главного меню:
        Распределить наряд - send_message_to_implementer()
        Список нарядов - give_orders_menu()
        Список сотрудников - give_employees_menu()
        Активные пользователи - give_list_of_active_users()

        Аргумент error используется для отправки сообщения пользователю
        о том, что он неправильно выбрал функцию с клавиатуры
        '''
        if error:
            super().send_message(self.id, 'Не понял вас! Повторите попытку,'
                                 ' используя всплывающую клавиатуру.', 
                                 reply_markup=self.main_keyboard)
        else:
            super().send_message(self.id, 'Главное меню',
                                 reply_markup=self.main_keyboard)


    def give_orders_menu(self, error=False):
        '''Возращает сообщение координатору и клавиатуру с выбором
        функции из меню нарядов:
        Активные наряды внедренцев - give_list_of_orders(kind='Акт...')
        Наряды внедренцев - give_list_of_orders(kind='Наряды внедр...')
        Наряды координатора - give_list_of_orders(kind='Наряды коо...')
        Назад - возвращает state к предыдущему состоянию из stack

        Ключевой аргумент error используется для отправки сообщения 
        пользователю, что он неправильно выбрал функцию с клавиатуры
        '''
        if error:
            super().send_message(self.id, 'Не понял вас! Повторите попытку,'
                                 ' используя всплывающую клавиатуру.', 
                                 reply_markup=self.lists_of_orders_keyboard)
        else:
            super().send_message(self.id, 'Какой список вы хотите получить?',
                                 reply_markup=self.lists_of_orders_keyboard)


    def give_employees_menu(self, error=False):
        '''Возращает сообщение координатору и клавиатуру с выбором
        функции из меню нарядов:
        Добавить сотрудника - add_employee()
        Удалить сотрудника - delete_employee()
        Назад - возвращает к предыдущему состоянию из self.stack

        Ключевой аргумент error используется для отправки сообщения 
        пользователю, что он неправильно выбрал функцию с клавиатуры
        '''
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
        elif kind == 'Наряды внедренцев':
            pass
        elif kind == 'Наряды координатора':
            super().send_message(self.id, 'Эти наряды вам следует '
                                 'распределить на внедренцев:')
            pass
        else:
            self.give_orders_menu(error=True)
            return
        self.give_main_menu()


    def give_list_of_active_users(self):
        '''Возращает список зарегистрированных пользователей, которые 
        начали работу с ботом (с помощью команды /start)
        '''
        super().send_message(self.id, 'Сегодня со мной уже связались:')
        for position in active_users.items():
            text = [position[0]]
            for employee in position[1].items():
                list_ = [employee[0], employee[1].name]
                text.append(' '.join(list_))
            text = '\n'.join(text)
            super().send_message(self.id, text)


    def give_list_of_employees(self):
        '''Возвращает список зарегистрированных пользователей.
        '''
        with open(PATH_ID_POSITION_NAME, encoding='UTF-8') as employees:
            text = employees.readlines()
        text = '\n'.join(text)
        self.send_message(self.id, text)


    def add_employee(self, message):
        '''Добавляет нового пользователя в систему по его id, position,
        name. В качестве подсказки координатору, возвращается список 
        пользователей, которые еще не зарегистрированы координатором, 
        но связались с ботом через команду /start.

        По умолчанию len(new_user) <= 10 (см. main.py).
        '''
        if self.state[2] == 0:
            self.cache = [None, None, None]
            super().send_message(self.id, 'Укажите id сотрудника, которого '
                                 'хотите добавить.')
            text = ['Этих пользователей я не знаю: ']
            for i in range(len(new_user)):
                text.append(' '.join(new_user.pop()))
            text = '\n'.join(text)
            super().send_message(self.id, text, 
                                 reply_markup=self.back_keyboard)
        elif self.state[2] == 1:
            self.cache[0] = message.text
            super().send_message(self.id, 'Укажите должность сотрудника', 
                                 reply_markup=self.position_keyboard)
        elif self.state[2] == 2:
            self.cache[1] = message.text
            super().send_message(self.id, 'Укажите ФИ сотрудника')
        elif self.state[2] == 3:
            self.cache[2] = message.text
            text = '\t'.join(self.cache) + '\n'
            with open(PATH_ID_POSITION_NAME, 'a', encoding='UTF-8') as employees:
                employees.write(text)
                super().send_message(self.id, 'Я добавил сотрудника:\n' + text)
                super().send_message(self.id, 'Изменения вступят в '
                                     'силу при следующем запуске бота!',
                                     reply_markup=self.continue_keyboard)


    def delete_employee(self, message):
        '''Удаляет пользователя из системы по его id.
        '''
        # Необходимо осуществить проверку в БД (НЕ в архиве), 
        # есть ли активные наряды, связанные с этим сотрудником. 
        # Добавить в issue на GitHub
        if self.state[2] == 0:
            super().send_message(self.id, 'Укажите id сотрудника, которого '
                                 'хотите удалить.')
        elif self.state[2] == 1:
            id_ = message.text
            with open(PATH_ID_POSITION_NAME, encoding='UTF-8') as employees:
                list_ = employees.readlines()
            new_list_ = [emp for emp in list_ if emp.find(id_)]
            with open(PATH_ID_POSITION_NAME, 'wt', encoding='UTF-8') as employees:
                employees.writelines(new_list_)
            super().send_message(self.id, 'Изменения вступят в '
                                 'силу при следующем запуске бота!', 
                                 reply_markup=self.continue_keyboard)

    
    def get_number_of_order(self, message):
        pass
    

    def get_implementer(self, message):
        pass


    def get_date_start_plan(self, message):
        pass


    def send_message_to_implementer(self, message):
        pass

    
    def run_state(self, message):
        '''Вызывает функцию, соответсвующую текущему состоянию
        (self.state) координатора.
        '''

        state = self.state
        if state[0] == 'Главное меню':
            if state[1] == 'Активные пользователи':
                self.give_list_of_active_users()
            self.give_main_menu()
        elif state[0] == 'Список сотрудников':
            if state[1] == 0:
                self.give_employees_menu()
                self.give_list_of_employees()
            elif state[1] == 'Добавить сотрудника':
                self.add_employee(message)
            elif state[1] == 'Удалить сотрудника':
                self.delete_employee(message)
        elif state[0] == 'Списки нарядов':
            if state[1] == 0:
                self.give_orders_menu()
            elif state[1] in {'Активные наряды внедренцев',
                              'Наряды внедренцев',
                              'Наряды координатора'}:
                self.give_list_of_orders(kind=state[1])
        elif state[0] == 'Распределить наряд':
            self.send_message_to_implementer(message)


    def change_state(self, message):
        '''Изменяет состояние (self.state) координатора, исходя из
        полученного сообщения (message) и текущего состояния. Если 
        message.text = 'Назад', то записывается предыдущее состояние.
        '''
        # final_step - число шагов в соответствующей функции, 
        # соответствующей состоянию. Надо будет убрать
        final_step = 2

        if message.text == 'Назад':
            if len(self.stack) > 1:
                self.stack.pop()
                self.state = self.stack[-1].copy()
        else:
            if self.state[0] == 'Главное меню':
                if message.text in {'Список сотрудников', 
                                    'Списки нарядов', 
                                    'Распределить наряд'}:
                    self.state[0] = message.text
                    self.state[1] = 0
                elif message.text == 'Активные пользователи':
                    self.state[1] = message.text
            elif self.state[0] == 'Список сотрудников':
                if self.state[1] == 0:
                    if message.text in {'Добавить сотрудника', 
                                        'Удалить сотрудника'}:
                        self.state[1] = message.text
                elif self.state[1] == 'Добавить сотрудника':
                    if self.state[2] == 3:
                        self.state = Coordinator.state.copy()
                    else:
                        self.state[2] += 1
                elif self.state[1] == 'Удалить сотрудника':
                    if self.state[2] == 1:
                        self.state = Coordinator.state.copy()
                    else:
                        self.state[2] += 1
            elif self.state[0] == 'Список нарядов':
                if message.text in {'Активные наряды внедренцев',
                                    'Наряды внедренцев',
                                    'Наряды координатора'}:
                    self.state[1] = message.text
                elif self.state[1] in {'Активные наряды внедренцев',
                                       'Наряды внедренцев',
                                       'Наряды координатора'}:
                    self.state = Coordinator.state.copy()
            elif self.state[0] == 'Распределить наряд':
                if self.state[1] == final_step:
                    self.state = Coordinator.state.copy()
                else:
                    self.state[1] += 1
                    
            self.stack.append(self.state.copy())
            if self.stack[-1] == Coordinator.state:
                self.stack = Coordinator.stack.copy()

        print(self.stack)
        print(self.state)


    def dialog_with_bot(self, message):
        
        self.change_state(message)
        self.run_state(message)





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

