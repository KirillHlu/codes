import random
import time
numbers = []
for i in range(1000000):
    numbers.append(random.randint(1, 9))
start_time = time.time()
numbers.sort(key = None, reverse=False)
end_time = time.time()
ex_time = end_time-start_time



def add_fine (nums):
    return [num + 5 for num in nums]
add_fine(numbers)
end_time = time.time()
ex_time_add = end_time-start_time
print(f"bubble_sort - {ex_time_add}")

def bubble_sort(nums):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i+ 1]:
                nums[i], nums[i + 1] = nums[i + 1],nums[i]
                swapped = add_fine(numbers)
