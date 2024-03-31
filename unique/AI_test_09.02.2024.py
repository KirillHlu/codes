№1
import math
import itertools
lst = ['1', '2', '3', '4']
res = list(itertools.permutations(lst, 3))
print(res)
print(math.factorial(3)*4)



№2
def func(M, N, perm):
    if M == 0:
        print(perm)
        return
    for i in range(N):
        perm.append(i)
        func(M - 1, N, perm)
        perm.pop()


M = int(input('M: '))
N = int(input("N: "))
N = N + 1
list = []
func(M, N, list)



№3
from more_itertools import distinct_permutations
x = [p for p in distinct_permutations(['Математика', 'Информатика', 'Русский язык', 'Информатика', 'Русский язык', 'Математика'],3)]
for item in x:
    print(item)
