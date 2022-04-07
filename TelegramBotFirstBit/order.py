
from datetime import date
import csv

# ����� ������������, ��� ����� ������� ��
# ���� ���������� ������, ������������ ���������� ������������
PATH_MANAGER = 'C:\\Users\\������\\Desktop\\manager.txt'

# ���� ���������� ������, ������������ ������������� ���������
PATH_COORDINATOR = 'C:\\Users\\������\\Desktop\\coordinator.txt'

# ���� ���������� �������� ������ ����������
PATH_IMPLEMENTER = 'C:\\Users\\������\\Desktop\\implementer.txt'

# ���� ���������� ������, ����������� ����������� (�����)
PATH_ARCHIVE = 'C:\\Users\\������\\Desktop\\data\\'


class Order(object):

    # ��� ���� �������� ��� ���� �����������, ������� ������� 
    # ��������� �� ������ ������ �� ����� PATH_COORDITATOR 
    
    def __init__(self, number_of_order, clients_name=None, date_manager=None,\
                 date_coordinator=None, date_start=None, date_finish=None,\
                 date_client=None, managers_name=None, implementers_name=None,\
                 description=None):
        self.number_of_order = number_of_order
        self.clients_name = clients_name
        self.date_manager = date_manager
        self.date_coordinator = date_coordinator
        self.date_start = date_start
        self.date_finish = date_finish
        self.date_client = date_client
        self.managers_name = managers_name
        self.implementers_name = implementers_name
        self.description = description


    def write_order(self):
        if self.date_finish:
            path = PATH_ARCHIVE + str(date.today()) + '.txt'
        elif self.date_start:
            path = PATH_IMPLEMENTER
        elif self.date_coordinator:
            path = PATH_COORDINATOR
        elif self.date_manager:
            path = PATH_MANAGER

        with open(path, 'a', encoding='UTF-8', newline='') as table:
            writer = csv.writer(table)
            list_ = [str(self.number_of_order).ljust(12),
                     str(self.clients_name).ljust(40),
                     str(self.date_manager).ljust(12),
                     str(self.date_coordinator).ljust(12),
                     str(self.date_start).ljust(12),
                     str(self.date_finish).ljust(12),
                     str(self.date_client).ljust(12),
                     str(self.managers_name).ljust(30),
                     str(self.implementers_name).ljust(30),
                     str(self.description).ljust(60),
                     ]
            writer.writerow(list_)


    def read_order(self):
        pass

        








