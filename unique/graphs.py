#1
a, b, c, d, e, f, g, h = range(8)

N = [
    {b:2, c:1, d:3, e:9, f:4},
    {d:8},
    {f:5},
    {f:1, h:6},
]

letters = ['a', 'b', 'c', 'd']
final_list = {}
index1 = 0
max_num = 0

for list1 in N:
    final_list[letters[index1]] = len(list1)
    index1 += 1

for key in final_list:
    if final_list[key] == max(final_list.values()):
        res = key

print(f'{res}: {max(final_list.values())}')



#2

import math
from random import *
import flet as ft
import flet.canvas as cv

v = 5
e = 4

list_x_y = []

for i in range(v*5000):
    list_1 = {}
    list_1[randint(1,1000)] = randint(1,500)
    list_x_y.append(list_1)

random_letters = ['a', 'b', 'c', 'c', 'e', 'f', 'g']

print(list_x_y)

def main(page: ft.Page):
    stroke_paint = ft.Paint(stroke_width=2, style=ft.PaintingStyle.STROKE)
    fill_paint = ft.Paint(style=ft.PaintingStyle.FILL)

    for  i in range(len(list_x_y)):
        for x, y, in list_x_y[i].items():
            try:
                for x2, y2 in list_x_y[i + 1].items():
                    try:
                        for x3, y3 in list_x_y[i+2].items():
                            cp = cv.Canvas(
                        [

                            cv.Circle(x, y, 25, paint=ft.Paint(
                                gradient=ft.PaintRadialGradient(
                                    ft.Offset(150, 150), 50, [ft.colors.BLUE_500, ft.colors.BLUE_500]
                                ),
                                style=ft.PaintingStyle.FILL,
                            )),
                            cv.Text(x, y, text=random_letters[randint(0, len(random_letters))]),
                            cv.Line(x + 25, y, x2, y2, paint=ft.Paint(
                                gradient=ft.PaintRadialGradient(
                                    ft.Offset(150, 150), 50, [ft.colors.BLUE_500, ft.colors.BLUE_500]
                                ),
                                style=ft.PaintingStyle.FILL,
                            ), ),
                            cv.Circle(x2 - 25, y2, 25, paint=ft.Paint(
                                gradient=ft.PaintRadialGradient(
                                    ft.Offset(150, 150), 50, [ft.colors.BLUE_500, ft.colors.BLUE_500]
                                ),
                                style=ft.PaintingStyle.FILL,
                            )),
                            cv.Text(x2-25, y2, text=random_letters[randint(0, len(random_letters))]),
                            cv.Line(x2, y2, x3, y3, paint=ft.Paint(
                                gradient=ft.PaintRadialGradient(
                                    ft.Offset(150, 150), 50, [ft.colors.BLUE_500, ft.colors.BLUE_500]
                                ),
                                style=ft.PaintingStyle.FILL,
                            ), ),
                        ],
                        width=float("inf"),
                        expand=True,)

                            page.add(cp)

                    except IndexError:
                        pass



            except IndexError:
                pass


ft.app(main)

#3
N = [
    {'b':2, 'c':1, 'd':3, 'e':9, 'f':4},
    {'d':8, 'c': 7},
    {'e':5, 'd': 5},
    {'e':1, 'h':6},
]

letters = ['a', 'b', 'c', 'd', 'e']
final_list = []
index1 = 0
max_items = [10000000]
final_list2 = []

while True:
    for list1 in N:
        for key, value in list1.items():
            try:
                if value < min(max_items) and key == letters[index1 + 1]:
                    max_items.append(value)

                else:
                    del key

            except IndexError:
                pass

        final_list.append(min(max_items))

        try:
            for key, value in list1.items():
                if value == min(max_items):
                    final_list2.append(f'{key}: {value}')

        except IndexError:
            pass

        max_items = [100000000]
        index1 += 1

    break

print(final_list2)
