from field import Field

class Name(Field):
    def __init__(self, name):
        if not len(name) >= 1:
            raise ValueError("Name should be at least 1 character long")
        super().__init__(name)
