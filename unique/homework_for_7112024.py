# №1

class Nikola:
    def __init__(self, name, age):
        if name == "Nikola":
            pass
        else:
            print(f"I am not {name}, i'm Nikola")

        self.__name = "Nikola"
        self.age = age

    def print_info(self):
        print(f"Name: {self.__name}\nAge: {self.age}")

person = Nikola('John', 15)
person.print_info()



# №2

class KgToPounds:
    def __init__(self, kg):
        self.__kg = kg

    def to_pounds(self):
        return self.__kg * 2.205

    @property
    def kg(self):
        return self.__kg

    @kg.setter
    def kg(self, value):
        self.__kg = value

a = KgToPounds(10)
print(a.kg)
print(a.to_pounds())
a.kg = 80
print(a.kg)
print(a.to_pounds())



# №3

class Phone:
    def __init__(self, number, model=None, weight=None):
        self.number = number
        self.model = model
        self.weight = weight

    def receive_call(self, name, caller_number=None):
        if caller_number:
            print(f"Calling {name}, number: {caller_number}")
        else:
            print(f"Calling {name}, number: none")

    def get_number(self):
        return self.number

    def send_message(self, phone_numbers):
        numbers = phone_numbers.split(';')
        print("Message sent to the following numbers:")
        for number in numbers:
            print(number)

phone1 = Phone("+7 923 531 45 58", "A 51", 200)
phone2 = Phone("+7 455 581 41 15", "A 52", 155)
phone3 = Phone("+7 854 452 14 15", "A 55", 180)

print(f"Phone first: Number: {phone1.number}, Model: {phone1.model}, Weight: {phone1.weight} g")
print(f"Phone second: Number: {phone2.number}, Model: {phone2.model}, Weight: {phone2.weight} g")
print(f"Phone third: Number: {phone3.number}, Model: {phone3.model}, Weight: {phone3.weight} g\n")

phone1.receive_call("John", phone1.number)
phone2.receive_call("Ssha", phone2.get_number())
phone3.receive_call('Bobby')

print("\n")

phone1.send_message(f"{phone2.get_number()}; {phone3.get_number()}")
