from collections import UserDict
from datetime import datetime, timedelta
from collections import defaultdict 
from copy import deepcopy, copy

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return 'No record found with this name'
        except TypeError:
            return 'Please provide full info'
        except AttributeError:
            return 'Contact not found'

    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = ''

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for index, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                self.phones[index] = Phone(new_phone)
                return 'Contact updated'
        return 'Contact doesn\'t have this phone'

    def find_phone(self, searched_phone):
        for phone in self.phones:
            if str(phone) == searched_phone:
                return str(phone)
            
    def add_birthday(self, birthday):
        try:
            self.birthday = datetime.strptime(birthday, "%d.%m.%Y")
            return 'Birthday added'
        except ValueError:
            return "Incorrect data format, should be DD.MM.YYYY"
        
    def show_birthday(self):
        try:
            return self.birthday.strftime('%d.%m.%Y')
        except:
            return 'Contact is missing birthday'
    
    def show_phones(self):
        return f"{'; '.join(p.value for p in self.phones)}"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
    
    def add_record(self, record):
        self.data[record.name.value] = record
        return 'Contact added'

    def delete(self, name):
        del self.data[name]

    def find(self,name):
        for key, record in self.data.items():
            if key == name:
                return record
            
    def get_birthdays_per_week(self):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        birthdays = defaultdict(list)
        result = ''

        def append_user(name, birthday):
            if today + timedelta(days = 1) <= birthday <= today + timedelta(days = 7):
                day_of_week = birthday.strftime('%A')

                if day_of_week in ['Saturday', 'Sunday']:
                    if 'Monday' in birthdays.keys():
                        birthdays['Monday'].append(name)
                    else:
                        birthdays['Monday'] = [name]
                else:
                    birthdays[day_of_week].append(name)

        for name, info in self.data.items():
            try:
                # update year to current for comparison
                append_user(name.title(), info.birthday.replace(year=datetime.now().year))
            except ValueError:
                # if Feb 29th doesn't exist, set to 28th
                append_user(name.title(), info.birthday.replace(year=datetime.now().year, day=28))
        
        for day, users in birthdays.items():
            result += f"{day}: {', '.join(users)}\n"

        if len(result) == 0:
            return 'No birthdays next week'

        return result
    
    def all_contacts(self):
        result = ''
        for key, value in self.data.items():
            print(value.birthday)
            result += f"Contact name: {key}, phones: {'; '.join(p.value for p in value.phones)}{', birthday: ' + value.birthday.strftime('%d.%m.%Y') if value.birthday else ''}"

        if len(result) == 0:
            return 'Address book is empty'
        
        return result

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def hello():
    return 'How can I help you?'

@input_error
def add_contact(args, book):
    name, phone = args
    if len(phone) != 10:
        return 'Phone should be 10 characters long'
    record = Record(name)
    record.add_phone(phone)
    return book.add_record(record)

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    if len(old_phone) != 10 or len(new_phone) != 10:
        return 'Phone should be 10 characters long'
    record = book.find(name)
    return record.edit_phone(old_phone, new_phone)

@input_error
def show_phone(args, book):
    name = args[0].lower()
    record = book.find(name)
    return record.show_phones()

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    return record.add_birthday(birthday)

@input_error
def show_birthday(args, book):
    name = args[0].lower()
    record = book.find(name)
    return record.show_birthday()

def main():
    book = AddressBook()

    methods = {
        'hello': hello,
        'add': add_contact,
        'change': change_contact,
        'phone': show_phone,
        'all': book.all_contacts,
        'add-birthday': add_birthday,
        'show-birthday': show_birthday,
        'birthdays': book.get_birthdays_per_week,
    }

    print('Welcome to the assistant bot!')

    while True:
        user_input = input('Enter a command:').strip().lower()
        command, *args = parse_input(user_input)

        if command in methods.keys():
            if (len(args) > 0):
                print(methods[command](args, book))
            else:
                print(methods[command]())
            continue

        if command in ['close', 'exit']:
            print("Good bye!")
            break

        print('Invalid command.')

if __name__ == "__main__":
    main()
