import numpy as np


def get_all_patterns():
    x = []
    for i in range(2 ** 20):
        binary_str = format(i, '020b')  # 20桁の2進数文字列を生成
        array = [int(bit) for bit in binary_str]
        x.append(array)
    return np.array(x)
