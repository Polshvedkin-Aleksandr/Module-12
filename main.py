from collections import UserDict
from collections.abc import Iterator
from datetime import datetime, date
import re
import pickle


class Field:
    __value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        # super().__init__()
        self.value = name


class Birthday(Field):
    def __init__(self, value: str):
        # super().__init__()
        try:
            d_m_y = re.split('[-,.: ]', value)
            if len(d_m_y[0]) == 4:
                d = int(d_m_y[2])
                y = int(d_m_y[0])
            else:
                d = int(d_m_y[0])
                y = int(d_m_y[2])
            m = int(d_m_y[1])
            v_date = date(year=y, month=m, day=d)
            self.value = v_date
        except Exception:
            self.value = ''


class Phone(Field):
    def __init__(self, value):
        try:
            if len(value) == 10:
                s = int(value)
                self.value = value
            else:
                print('phone number is not 10 digits ')
                self.value = ''
        except ValueError:
            print("Number not valid")
            self.value = ''


class Record:
    def __init__(self, name, birthday=""):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.current_value = 0

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday.value == "":
            return f'День Рождения {self.name.value} не известен.'
        date_v = self.birthday.value
        date_now = datetime.now()
        d1 = date(year=int(date_now.year), month=int(
            date_v.month), day=int(date_v.day))
        d0 = date(year=int(date_now.year), month=int(
            date_now.month), day=int(date_now.day))
        diferense = d1-d0
        res = diferense.days
        if res < 0:
            d1 = date(year=(int(date_now.year)+1), month=int(
                date_v.month), day=int(date_v.day))
            diferense = d1-d0
            res = diferense.days
        return f'до Дня Рождения {self.name.value} осталось {res} день(дней)'

    def add_phone(self, new_phone):
        new = Phone(new_phone)
        if new.value != '':
            self.phones.append(new)
            return {self.name: self.phones}

    def remove_phone(self, del_phone):
        for phone in self.phones:
            if phone.value == del_phone:
                self.phones.remove(phone)
        return {self.name: self.phones}

    def edit_phone(self, phone, new_phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                self.phones[i] = Phone(new_phone)
                return {self.name: self.phones}
        raise ValueError

    def find_phone(self, phone):
        for i in range(len(self.phones)):
            if phone == self.phones[i].value:
                return f"{self.phones[i]} in {self.name} "

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"


class AddressBook(UserDict):
    def __init__(self, max=20):
        self.page = 1
        self.MAX_VALUE = max
        self.current_value = 0
        self.data = {}

    def __next__(self):
        d = list(self.data)

        if self.MAX_VALUE > len(d):
            self.MAX_VALUE = len(d)
        if ((self.current_value < self.MAX_VALUE) and (len(d)) >= (self.MAX_VALUE-self.current_value)):
            key = d[self.current_value]
            self.current_value += 1
            return self.data[key]
        else:
            print("{:_^100}".format(self.page))
            self.page += 1
            self.MAX_VALUE = self.MAX_VALUE+self.MAX_VALUE

        raise StopIteration

    def __iter__(self) -> Iterator:
        return self

    def add_record(self, new):
        self.data.update({new.name.value: new})

    def find(self, find_name):
        if find_name in self.data:
            return self.data[find_name]

    def delete(self, del_name):
        if del_name in self.data:
            self.data.pop(del_name)

    def open_addressbook(self, filename):
        try:
            with open(filename, "rb") as fh:
                unpacked = pickle.load(fh)
        except FileNotFoundError:
            unpacked = AddressBook()
            print('Creating a new Addressbook')
        return unpacked

    def save_addressbook(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)

    def find_in_book(self, value: str):
        value = str(value)               # if value is digits
        result = []
        for contact, record in self.data.items():
            if value in contact:
                result.append(record)
            for phone in record.phones:
                if value in phone.value:
                    if record in result:
                        pass
                    else:
                        result.append(record)
        if result != []:
            print("Match in Addressbok:")
        else:
            print("No match found")
        for cont in result:
            print(f'-{cont}')
        return result
