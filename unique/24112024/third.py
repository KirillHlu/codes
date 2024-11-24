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
