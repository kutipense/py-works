def sezar(text):
    return ''.join(map(lambda x: chr(ord(x)+13 if ord(x)<=77 else ord(x)-13),text))

print(sezar('VUE VUE VUE'))
print(sezar('IHR IHR IHR'))
