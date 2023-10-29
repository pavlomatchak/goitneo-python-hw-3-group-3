from address_book import AddressBook
from record import Record

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
        'hello': hello(),
        'add': add_contact,
        'change': change_contact,
        'phone': show_phone,
        'all': book.__str__,
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
