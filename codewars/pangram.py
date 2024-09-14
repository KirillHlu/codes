def is_pangram(st):
    str1 = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
    was = []
    count = 0
    answer = False
    for letter in st.lower():
        if letter in str1 and letter not in was:
            count+=1
            was.append(letter)
            
    if count == len(str1):
         return True
        
    return answer
