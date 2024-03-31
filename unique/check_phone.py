import re
text = "+7 923 300 30 30"
digits = re.findall(r'\d', text)
digitss = re.findall(r'\D', text)
def check(number):
    digits = re.findall(r'\d', text)
    symbol = re.findall(r'\D', text)
    digits2 = re.findall(r'\d', number)
    symbol2 = re.findall(r'\D', number)
    if digits[0:2] == digits2[0:2] and symbol == symbol2:
        print('True')
    else:
        print("Isn't true")
check(input('Enter your number:'))
