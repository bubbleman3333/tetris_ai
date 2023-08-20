import numpy as np

x = np.array([3, 2, 1, 4, 3, 1, 2, 23, 5])

min_idx = np.argmin(x)

ans = np.delete(x, min_idx)
print(ans)
