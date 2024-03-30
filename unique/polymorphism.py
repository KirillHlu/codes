class Rectangle():
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
    def info(self):
        print(f'This is the area of the rectangle ({self.num1}, {self.num2})')

    def action(self):
        print(f'{self.num1} * {self.num2} = {self.num1*self.num2}')

class Triangle():
    def __init__(self, num1, num2, num3):
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3
    def info(self):
        print(f'This is the area of the triangle ({self.num1}, {self.num2}, {self.num3})')

    def action(self):
        s = (self.num1+self.num2+self.num3)/2
        print((s * (s - self.num1) * (s - self.num2) * (s - self.num3))**0.5)

class Cube():
    def __init__(self, num1, num2, num3):
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3

    def info(self):
        print(f'This is the volume of the cube ({self.num1}, {self.num2}, {self.num3})')

    def action(self):
        print(f'{self.num1} * {self.num2} * {self.num3} = {self.num1 * self.num2 * self.num3}')


print('\nFor rectangle: ')
squere1 = Rectangle(int(input('Num1: ')),int(input('Num2: ')))
print('\nFor triangle: ')
squere2 = Triangle(int(input("Num1: ")),int(input('Num2: ')),int(input('Num3: ')))
print("\nFor the volume of the cube:")
volume1 = Cube(int(input("Num1: ")),int(input('Num2: ')),int(input('Num3: ')))


for actions in (squere1, squere2, volume1):
    actions.info()
    actions.action()
