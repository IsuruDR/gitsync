class Animal:
    __name = ""
    __height = 0
    __speed = 0

    def __init__(self, name, height, speed):
        self.__name = name
        self.__height = height
        self.__speed = speed

    def set_name(self, name):
        self.__name = name

    def set_height(self, height):
        self.__height = height

    def set_speed(self, speed):
        self.__speed = speed

    def get_name(self):
        return self.__name

    def get_height(self):
        return self.__height

    def get_speed(self):
        return self.__speed

    def to_string(self):
        return 'name {} height {} speed {}'.format(self.__name, self.__height, self.__speed)
