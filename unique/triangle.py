size = int(input("Введите длину: "))
a = input("Введите символ: ")
for i in range(size):
    for j in range(size - i - 1):
        print(' ', end='')
    for k in range(2 * i + 1):
        print(a, end='')
    print()
