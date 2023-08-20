import hashlib
import numpy as np

def hash_array(arr):
    arr_bytes = arr.tobytes()
    hash_obj = hashlib.sha256(arr_bytes)
    return hash_obj.digest()

c = np.array([1, 1, 1])

p = hash_array(c)

print(p)

t = p.hex()  # バイト列を16進数文字列に変換

print(t)

c_decoded = bytes.fromhex(t)  # 16進数文字列をバイト列に変換

print(c_decoded == p)
