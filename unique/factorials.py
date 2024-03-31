#1
import math
print(math.factorial(5))


#2
def factorial(n):
    if n == 1:
        return 1    
    else:
        return n * factorial(n-1)
print(factorial(3)*2)

#3
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)
print(factorial(4)//2)

#4
def factorial(n):
    if n == 1:
        return 1    
    else:
        return n * factorial(n-1)
print(factorial(4)//2)
