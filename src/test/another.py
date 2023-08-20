import numpy as np

height = 20
array = np.random.randint(2, size=(height, 10))

print(array)


from time import time

start = time()

for i in range(1000):
    p = np.argmax(array, axis=0)
    p[np.max(array, axis=0) == 0] = height
    p = 4 - p

    diff = np.diff(p)

print(time()-start)
