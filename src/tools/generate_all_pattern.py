import numpy as np
import json
import hashlib


def hash_array(arr):
    arr_bytes = arr.tobytes()  # 配列をバイト列に変換
    hash_obj = hashlib.sha256(arr_bytes)  # SHA-256ハッシュオブジェクトを作成
    return hash_obj.digest()


def get_holes(s):
    one = False
    ans = 0
    for i in s:
        if one and i == "0":
            ans += 1
        elif i == "1":
            one = True
    return ans


def get_all_patterns():
    dic = {}
    for i in range(2 ** 20):
        binary_str = format(i, '020b')  # 20桁の2進数文字列を生成
        hole_num = get_holes(binary_str)
        array = np.array([int(bit) for bit in binary_str]).astype(int)
        hash_ = hash_array(array).hex()
        dic[hash_] = hole_num
    return dic


x = get_all_patterns()
temp = r"C:\Users\aiueo\tetris_ai\conf_files\test.json"

with open(temp, "wt", encoding="utf-8") as f:
    json.dump(x, f, indent=2, ensure_ascii=False)
