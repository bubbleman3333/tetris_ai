import json
import pickle

import numpy as np

four_base = (np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]), np.array([4, 5, 6, 7] * 4))
three_base = (np.array([0, 0, 0, 1, 1, 1, 2, 2, 2]), np.array([4, 5, 6] * 3))
two_base = (np.array([0, 0, 1, 1]), np.array([4, 5] * 2))

p = np.arange(100).reshape((10, 10))

dic = {
    2: two_base,
    3: three_base,
    4: four_base
}

piece_size = {k: 3 for k in range(1, 7) if k != 3
              }
piece_size[3] = 2
piece_size[7] = 7

from src.confs import base_config

piece_color = {
    0: "#ffffff",
    1: "#ffa500",
    2: "#0000ff",
    3: "#ffff00",
    4: "#800080",
    5: "#ff0000",
    6: "#00ff00",
    7: "#00ffff"
}

pieces = {
    1: np.array([
        [0, 0, 0],
        [0, 0, 1],
        [1, 1, 1]
    ]),
    2: np.array([
        [0, 0, 0],
        [2, 0, 0],
        [2, 2, 2]
    ]),
    3: np.array([
        [3, 3],
        [3, 3]
    ]),
    4: np.array([
        [0, 0, 0],
        [0, 4, 0],
        [4, 4, 4]
    ]),
    5: np.array([
        [0, 0, 0],
        [5, 5, 0],
        [0, 5, 5]
    ]),
    6: np.array([
        [0, 0, 0],
        [0, 6, 6],
        [6, 6, 0]
    ]),
    7: np.array([
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
    ])
}

with open(base_config.CONF_PATH / "piece_dict.pkl", "wb") as f:
    pickle.dump(pieces, f)

with open(base_config.CONF_PATH / "piece_color.json", "wt") as f:
    json.dump(piece_color, f)
