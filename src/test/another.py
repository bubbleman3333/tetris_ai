import numpy as np


def aiueo(xx):
    xx += 1
    return xx


p = np.zeros(10)
c = p.copy()
c[1] = 1

print(np.all(p == 0))
print(np.all(c == 0))
