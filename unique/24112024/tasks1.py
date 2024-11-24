#1

class Soda():
    def __init__(self, additive=None):
        self.additive = additive

    def show_my_drink(self):
        if self.additive == None or len(self.additive.split()) == 0:
            print(f"Usually soda")
        else:
            print(f"Soda and {self.additive}")

soda = Soda("sugar")
soda.show_my_drink()

#2

class TriangleChecker():
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def is_triangle(self):
        try:
            if min([self.side1, self.side2, self.side3]) >= 0:
                print("Yeah, we can build a triangle!")
            else:
                print("Nothing will work with negative numbers!")

        except TypeError:
            print("You only need to enter numbers!")

triangle = TriangleChecker(1, 5, 4)
triangle.is_triangle()

#3

class Math():
    def __init__(self, a, b):
        if type(a) != str and type(b) != str:
            self.a = a
            self.b = b
        else:
            print("Enter your nums correctly!")
            self.a = None
            self.b = None

    def addition(self):
        if self.a != None and self.b != None:
          print(f"Addition: {self.a + self.b}")

    def multiplication(self):
        if self.a != None and self.b != None:
          print(f"Multiplication: {self.a * self.b}")

    def division(self):
        if self.a != None and self.b != None:
          print(f"Division: {self.a / self.b}")

    def subtraction(self):
        if self.a != None and self.b != None:
          print(f"Subtraction: {self.a - self.b}")


math = Math(5, 4)
math.addition()
math.multiplication()
math.division()
math.subtraction()
