import math
from itertools import permutations
word = 'толпа'
all_combinations = [''.join(p) for p in permutations(word)]
print(math.factorial(len(word)))
print(all_combinations)
