import abc
class Animal(abc.ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    @abc.abstractmethod
    def say(self): pass

    @abc.abstractmethod
    def info(self): pass

    @abc.abstractmethod
    def set_age(self, age): pass


class Cat(Animal):
    def set_age(self, age):
        if 0 < age < 30:
            self.__age = age
    def say(self):
        print(f'{self.name}: meow')

    def info(self):
        print(f'Name: {self.name}, Age: {self.age}')



class Dog(Animal):
    def set_age(self, age):
        if 0 < age < 30:
            self.age = age
        else:
            self.age = 'None'

    def say(self):
        print(f'{self.name}: GAV GAV')

    def info(self):
        print(f'Name: {self.name}, Age: {self.age}')

dog = Dog('Bobby', 'None')
dog.set_age(100)
dog.say()
dog.info()

