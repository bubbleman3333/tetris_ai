import numpy as np
from collections import defaultdict


def select_random_with_bias(lst):
    weights = np.exp(np.arange(len(lst))[::-1])  # 先頭にある方がより大きな重みを持つように指数関数を適用
    selected_indices = np.random.choice(len(lst), size=2, replace=False, p=weights / np.sum(weights))
    return [lst[i] for i in selected_indices]


dic = defaultdict(int)
# 例
my_list = list(range(50))

for _ in range(1000):
    selected_elements = select_random_with_bias(my_list)
    for i in selected_elements:
        dic[i] += 1
print(dic)
