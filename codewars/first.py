def alphabet_position(text):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']

    out = ""

    for word in text.split():
        for letter in word:
            if letter.lower() not in letters:
                pass
            else:
                index1 = letters.index(letter.lower()) + 1
                out = out + f' {index1}'

    return out.strip()
