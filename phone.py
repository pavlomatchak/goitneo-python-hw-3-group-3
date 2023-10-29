from field import Field

class Phone(Field):
    def __init__(self, phone):
        if not (len(phone) == 10 and phone.isdigit()):
            raise ValueError("Phone should be 10 digits long")
        super().__init__(phone)
