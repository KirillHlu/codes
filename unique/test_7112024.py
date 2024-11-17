#1

list1 = [6, -5, 85, -100]
list2 = []

for el in list1:
    list2.append(abs(el))

print(f'Max: {max(list2)}\nMin: {min(list2)}')


#2

list1 = [5, 8, 4, -8, 8]
list1 = sorted(list1)

if list1[-1] == list1[-2]:
    print("Wrong!")
else:
    print(f'First: {list1[-1]}\nSecond: {list1[-2]}')

#3

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def pre_order(node):
    if node:
        print(node.value)
        pre_order(node.left)
        pre_order(node.right)

tree = TreeNode(1)
tree.left = TreeNode(2)
tree.right = TreeNode(3)
tree.left.left = TreeNode(4)
tree.left.right = TreeNode(5)
pre_order(tree)
