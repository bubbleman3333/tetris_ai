import numpy as np

p = np.array([[
    0,
    0,
    0,
    1
],
    [
        1,
        0,
        -1,
        0
    ]
])

start = np.array([[0], [1]])

now = start + p
print(now)

right = np.array([[0], [1]])

y, x = now

max_x, min_x = x.max(), x.min()
# for i in range(-min_x, 19 - max_x+1):
#     print(i)
#     temp = now + right * i
#     print(temp)

for i in range(10-max_x):
    print(i)
    temp = now + right * i
    print(temp)
