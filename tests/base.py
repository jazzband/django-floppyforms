import django

class InvalidVariable(str):
    def __bool__(self):
        return False
