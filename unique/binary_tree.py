class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def task_first(node):
    if node:
        print(node.value)
        task_first(node.left)
        task_first(node.right)

def task_second(node):
    if node:
        print(node.value)
        task_second(node.right)
        task_second(node.left)

tree = TreeNode(1)
tree.left = TreeNode(2)
tree.right = TreeNode(3)
tree.left.left = TreeNode(4)
tree.left.right = TreeNode(5)
print('First:\n')
task_first(tree)
print('\nSecond:\n')
task_second(tree)
