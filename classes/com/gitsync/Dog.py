from classes.com.gitsync.Animal import Animal


class Dog(Animal):
    __owner = ""

    def __init__(self, owner, name, height, speed):
        self.__owner = owner
        super(Dog, self).__init__(name, height, speed)

    def set_owner(self, owner):
        self.__owner = owner
