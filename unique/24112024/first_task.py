class Student():
    def __init__(self, firstName=None, lastName=None, group=None, averageMark=None):
        self._firstName = firstName
        self._lastName = lastName
        self._group = group
        self._averageMark = averageMark

    def getScholarship(self):
        if self._averageMark >= 4.6:
            print("5000 ₸")
        else:
            print("500 ₸")


class Aspirant(Student):
    def getScholarship(self):
        if self._averageMark >= 4.6:
            print("6000 ₸")
        else:
            print("600 ₸")

john = Student("John", "Somelastname", 'group4', 5)
sasha = Aspirant("Sasha","anotherLastname", "group7", 4)

for el in (john, sasha):
    el.getScholarship()
