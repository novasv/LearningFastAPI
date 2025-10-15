import random
import string

c = 1
l = []
caracteres_possiveis = string.ascii_letters + string.digits
for c in range(0,20):
    value = ''.join(random.choices(caracteres_possiveis))
    l.append(value)
    print(f'{value}', end=' ')


