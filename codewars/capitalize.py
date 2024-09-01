def to_jaden_case(string1):
    out = ''
    string = string1.split()
    for el in string:
        out = out + f' {el.capitalize()}'

    return out.strip()
