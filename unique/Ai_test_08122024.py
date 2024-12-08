#1
class Car:
    def __init__(self, mark, age, color):
        self.__mark = mark
        self.__age = age
        self.__color = color

    def get_mark(self):
        return self.__mark

    def set_mark(self, mark):
        self.__mark = mark

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if age >= 1885 and age <= 2024:
            self.__age = age
        else:
            print("Wrong age!")

    def get_color(self):
        return self.__color

    def set_color(self, color):
        self.__color = color

car1 = Car("Some_mark", 1975, "black")
car1.set_age(20000)
print(car1.get_age())


#2
class Human:
    def __init__(self, name, age, gender):
        self._name = name
        self._age = age
        self._gender = gender

    def show_information(self):
        print(f"Human: \n  Name: {self._name}\n  Age: {self._age}\n  Gender: {self._gender}")
    def set_age(self, age):
        if age >= 0 and age <= 150:
            self.__age = age
        else:
            print("Wrong age!")

    def get_age(self):
        return self.__age

    def get_name(self):
        return self._name

    def get_gender(self):
        return self._gender

class Schoolboy(Human):
    def __init__(self, name, age, gender, diary, record_book):
        Human.__init__(self, name, age, gender)
        self.diary = diary
        self.record_book = record_book

    def show_information(self):
        print(f"Schoolboy: \n  Name: {self._name}\n  Age: {self._age}\n  Gender: {self._gender}\n  Diary: {self.diary.grades}\n  Record book: {self.record_book.final_grades}")


class Student(Human):
    def __init__(self, name, age, gender, diary, record_book):
        Human.__init__(self, name, age, gender)
        self.diary = diary
        self.record_book = record_book

    def show_information(self):
        print(f"Schoolboy: \n  Name: {self._name}\n  Age: {self._age}\n  Gender: {self._gender}\n  Diary: {self.diary.grades}\n  Record book: {self.record_book.final_grades}")

class Diary:
    def __init__(self, grades):
        self.grades = grades

class Record_book:
    def __init__(self, final_grades):
        self.final_grades = final_grades

diary1 = Diary([5,4,4,5,4,4,4,4,3 ,5, 5])
record_book = Record_book([5,4,5,5,4,5,4,4,4,5])
first_student = Student("John", 25, "Male", diary1, record_book)
print(first_student.get_name())

diary2= Diary([5,4,4,5,4,4,4])
record_book2 = Record_book([5,4,5,5,4,5])
schoolboy = Schoolboy("Sasha", 25, "Male", diary1, record_book)
print(first_student.get_name())

print(f"\n\n\n Third task:"
      f"\n")

Human("dd", 4, "d").show_information()
print()
schoolboy.show_information()
