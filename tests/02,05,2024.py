import math
import flet as ft
import flet.canvas as cv

class Circle():
    def __init__(self, radius):
        self.radius = radius

    def square(self):
        r = float(self.radius)
        p = 2 * math.pi * r
        s = math.pi * math.pow(r, 2)
        print(f'Square of circle = {s:.2f}')

    def show_circle(self):
        def main(page: ft.Page):

            stroke_paint = ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE, color='Blue')
            fill_paint = ft.Paint(style=ft.PaintingStyle.FILL)
            cp = cv.Canvas(
                [
                    cv.Circle(100, 90, 50, stroke_paint),
                    cv.Circle(1000, 90, 10, stroke_paint),
                ],
                width=float("inf"),
                expand=True,
            )

            page.add(cp)
        ft.app(main)

class Rect():
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2

    def square(self):
        a = int(self.side1)
        b = int(self.side2)
        print(f'Square of rectangle: {a*b}')


circle = Circle(input(f'Radius: '))
rect = Rect(int(input('First side: ')),int(input('Second side: ')))

for i in (circle, rect):
    i.square()

circle.show_circle()
