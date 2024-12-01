#!
import json


class Animals:
    def __init__(self, name, age, color):
        self.name = name
        self.age = age
        self.color = color

    def information(self):
        print(f"{self.name}: {self.age}, {self.color}")

class Dog(Animals):
    def __init__(self, name, age, color):
        Animals.__init__(self, name, age, color)
        self.type_of_animals = "Dog"

    def sound(self):
        print("Dog: brug brug")

class Eagle(Animals):
    def __init__(self, name, age, color):
        Animals.__init__(self, name, age, color)
        self.type_of_animals = "Eagle"

    def sound(self):
        print("Eagle: raahhh")

class Cat(Animals):
    def __init__(self, name, age, color):
        Animals.__init__(self, name, age, color)
        self.type_of_animals = "Cat"

    def sound(self):
        print("Cat: meow")


list_of_animals = [Dog("Bobby", 4, "black"), Eagle('Bob', 2, 'brown'), Cat("Somename", 6, "white")]
list_of_animals_2 = {}

for animal in list_of_animals:
    animal.sound()
    list_of_animals_2[animal.type_of_animals] = {"Name": animal.name, "Age": animal.age, "Color": animal.color}

print(list_of_animals_2)

with open('data1.json', 'w') as json_file:
    json.dump(list_of_animals_2, json_file)

#2
import flet as ft


class Table:
    def __init__(self, height, width, type_of_table):
        self.height = height
        self.width = width
        self.type_of_table = type_of_table


class Circle_table(Table):
    def __init__(self, height, width, type_of_table, radius):
        super().__init__(height, width, type_of_table)
        self.radius = radius

    def square(self):
        return 3.14 * (self.radius ** 2)


class Rectangle_table(Table):
    def __init__(self, height, width, type_of_table, first_side, second_side):
        super().__init__(height, width, type_of_table)
        self.first_side = first_side
        self.second_side = second_side

    def square(self):
        return self.first_side * self.second_side


class Final_table(Table):
    def __init__(self, height, width, type_of_table, radius=None, first_side=None, second_side=None):
        super().__init__(height, width, type_of_table)
        self.radius = radius
        self.first_side = first_side
        self.second_side = second_side

    def square(self):
        if self.type_of_table == "circle":
            return Circle_table(self.height, self.width, self.type_of_table, self.radius).square()
        else:
            return Rectangle_table(self.height, self.width, self.type_of_table, self.first_side,
                                   self.second_side).square()


def main(page: ft.Page):
    def reload(e):
        input_height.value = None
        input_width.value = None
        input_radius.value = None
        input_type_of_table.value = None
        page.clean()
        page.add(input_type_of_table, btn, btn3)

    def main_fun1(e):
        try:
            radius_value = float(input_radius.value)
            square = Final_table(1, 1, input_type_of_table.value, radius=radius_value).square()
            page.add(ft.Text(f"{square}"))
        except ValueError:
            page.add(ft.Text("Enter your data correctly!"))

    def main_fun2(e):
        try:
            first_side_value = float(input_width.value)
            second_side_value = float(input_height.value)
            square = Final_table(1, 1, input_type_of_table.value, first_side=first_side_value,
                                 second_side=second_side_value).square()
            page.add(ft.Text(f"{square}"))
        except ValueError:
            page.add(ft.Text("Enter your data correctly!"))

    def choice_table(e):
        choice1 = input_type_of_table.value
        page.clean()

        if choice1 == "circle":
            page.add(input_radius, btn1, btn3)
        elif choice1 == "rectangle":
            page.add(input_height, input_width, btn2, btn3)
        else:
            page.add(input_type_of_table, btn, btn3)

    page.title = 'Table'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    input_type_of_table = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option("circle"),
            ft.dropdown.Option("rectangle"),
        ],
    )

    input_height = ft.TextField(label="Height", width=300)
    input_width = ft.TextField(label='Width', width=300)
    input_radius = ft.TextField(label="Radius", width=300)

    btn = ft.ElevatedButton(text="Submit", on_click=choice_table)
    btn1 = ft.ElevatedButton(text="Submit", on_click=main_fun1)
    btn2 = ft.ElevatedButton(text="Submit", on_click=main_fun2)
    btn3 = ft.ElevatedButton(text="Reload", on_click=reload)


    page.add(input_type_of_table, btn, btn3)


ft.app(target=main)

#3
class Means_of_transportation():
    def __init__(self, mark, model, age):
        self.mark = mark
        self.model = model
        self.age = age

    def show_short_information(self):
        print(f"{self.model}:\nMark: {self.mark}\nAge: {self.age}")

class Category():
    def __init__(self, type_of_category, list_of_category):
        self.type_of_category = type_of_category
        self.list_of_category = list_of_category

    def show_categories(self):
        print(f"{self.type_of_category}:")
        for el in self.list_of_category:
            print(f"  {el.model}: \n    Mark: {el.mark}\n    Age: {el.age}")

class Plain(Means_of_transportation):
    def main_action(self):
        print(f"{self.model} starts to fly!")

class Car(Means_of_transportation):
    def main_action(self):
        print(f"{self.model} starts to go!")

first_object = Means_of_transportation('Some mark', "somemodel", 80)
second_object = Means_of_transportation('Someeeeee mark', "somemodel", 8080)

third_object = Means_of_transportation('Some plain mark', "some model 14", 50)
fourth_object = Means_of_transportation('Some plain mark', "some model 154", 10)

category1 = Category("Cars", [first_object, second_object])
category2 = Category("Plains", [third_object, fourth_object])

for el in (category1, category2):
    print('\n')
    el.show_categories()
    print("\n")

for el in (Plain('Some mark', 'Some model4', 4), Car('some mark', 'some model5', 8)):
    el.main_action()
