import math
import itertools
a = input('Enter your word or nums: ')
perm_set = itertools.permutations(a)
for val in perm_set: print(val)
print(math.factorial(len(a)))
