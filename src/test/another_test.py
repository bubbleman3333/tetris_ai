import numpy as np
import json
from src.confs import base_config

t = np.array([[0, 1], [0, 0], [0, -1], [1, 0]])
i = np.array([[-1, 0], [0, 0], [1, 0], [2, 0]])
s = np.array([[0, -1], [0, 0], [1, 0], [1, 1]])
z = np.array([[0, 1], [0, 0], [1, 0], [1, -1]])
o = np.array([[0, -1], [0, 0], [1, 0], [1, -1]])
j = np.array([[-1, 0], [0, 0], [0, 1], [0, 2]])
l = np.array([[-1, 0], [0, 0], [0, -1], [0, -2]])

minos = [t, i, s, z, o, j, l]
# rotation_matrix = np.array([[0, -1], [1, 0]])
# x = np.array([1,3])+t
# print(x)
# for mino in minos:
#     mean = mino.mean(axis=0)
#
#     answer = np.dot(rotation_matrix, mino.T).T

dic = {idx + 1: val.T.tolist() for idx, val in enumerate(minos)}

with open(base_config.CONF_PATH / "minos.json", "wt", encoding="utf-8") as f:
    json.dump(dic, f, indent=4)
