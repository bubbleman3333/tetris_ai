import numpy as np

x = np.zeros((3,3))


def get_copy(b):
    b = b.copy()
    b[b<1] = 1
    return b

print(x)

t = get_copy(x)
print(t)
print(x)