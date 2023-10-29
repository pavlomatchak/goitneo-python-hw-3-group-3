from name import Name
from phone import Phone
from datetime import datetime

class Record:
    def __init__(self, name):
        try:
            self.name = Name(name)
        except ValueError as e:
            print(e)
        self.phones = []
        self.birthday = ''

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(e)

    def edit_phone(self, old_phone, new_phone):
        for index, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                try:
                    self.phones[index] = Phone(new_phone)
                except ValueError as e:
                    print(e)
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
