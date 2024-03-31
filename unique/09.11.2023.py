f = open('teeext')
s = f.read()
print(s.count( 'b'))
count = 0
max_b = 0
for b in s:
    if b == "b":        
        max_b += 1
    if count > max_b:        
        max_b = count
    else:        
        count = 0
print("Максимальное кол-во идущих подряд b ", max_b)
