import re

def order(sentence):
    sentence = sentence.split()
    list1 = {}
    final_str = ''

    for word in sentence:
        nums = re.findall(r'\d', word)
        num = ''
        for digital in nums:
            num = num + str(digital)
        num = int(num)

        list1[num] = word

    for word in sorted(list1):
        if len(final_str) == 0:
            final_str = final_str + '' + str(list1[word])
        else:
            final_str = final_str + ' ' + str(list1[word])

    return final_str

print(order('c1ase a2s 3it b4e h5is kno6w ow7n c8ompany'))
