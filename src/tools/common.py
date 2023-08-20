import hashlib
import numpy as np


def hash_array(arr):
    arr_bytes = arr.tobytes()  # 配列をバイト列に変換
    hash_obj = hashlib.sha256(arr_bytes)  # SHA-256ハッシュオブジェクトを作成
    return hash_obj.digest()


def softmax(x):
    e_x = np.exp(x - np.max(x))  # オーバーフローを防ぐための安全な実装
    return e_x / e_x.sum()
