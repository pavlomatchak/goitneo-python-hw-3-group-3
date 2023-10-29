from collections import UserDict
from datetime import datetime, timedelta
from collections import defaultdict 

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
    
    def __str__(self):
        result = ''
        for key, value in self.data.items():
            print(value.birthday)
            result += f"Contact name: {key}, phones: {'; '.join(p.value for p in value.phones)}{', birthday: ' + value.birthday.strftime('%d.%m.%Y') if value.birthday else ''}\n"

        if len(result) == 0:
            return 'Address book is empty'
        
        return result
