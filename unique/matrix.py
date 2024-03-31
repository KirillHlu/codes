width = int(input('Enter the width of matrix: '))
hight = int(input('Enter the height of matrix: '))
a = int(input())
matrix = [[a for i in range(width)] for i in range(hight)]
for i in matrix:
    for j in i:
        print(j, end='\t')
    print()
