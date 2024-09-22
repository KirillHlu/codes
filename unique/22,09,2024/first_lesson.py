#1
from random import *
list1 = [randint(1,80) for i in range(8)]
print(f'{list1[0]} {list1[-1]}')

#2
list1 = [1, 2, 3, 4, 3, 2, 1]
if list(reversed(list1[(len(list1)//2):])) == list1[0:((len(list1)//2)+1)]:
    print('True')
else:
    print('False')

#3
list1 = list(range(5,15))
list2 = list(range(8,15))
final_list = []

for el in list1:
    if el not in list2:
        final_list.append(el)

print(final_list)

#4
def change(list1):
    first_el = list1[0]
    last_el = list1[-1]

    list1[0] = last_el
    list1[-1] = first_el

    return list1

print(change([5,4,5,8,9,7]))

#5
def list_sort(list1):
    final_list = []
    for i in list(reversed(sorted(list1))):
        final_list.append(i)

    return final_list

print(list_sort([4,5,8,7,5,]))
