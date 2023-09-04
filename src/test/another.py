import numpy as np

row = 5
x = np.random.randint(0, 2, (row, 3))

print(x)

one_located_max = np.argmax(x, axis=0)

print(one_located_max)
max_idx = max(one_located_max)
print(x[:max_idx])
invalid_rows = row - max_idx
print(invalid_rows,"行")
