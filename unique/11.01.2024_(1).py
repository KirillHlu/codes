spisok = [1, 2, 3]
spisok2 = []
for digit in spisok:
    int(digit)
    if digit == max(spisok):
        spisok.remove(digit)
        spisok2.append(digit)
    for digit in spisok:
        int(digit)
        if digit == max(spisok):
            spisok.remove(digit)
            spisok2.append(digit)

print(spisok2)
