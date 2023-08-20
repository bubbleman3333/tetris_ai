import pickle
import json
from src.confs import base_config
import numpy as np


class TetrisConfLoader:

    @staticmethod
    def get_piece_color_dict():
        with open(base_config.CONF_PATH / "piece_color.json", "rt") as f:
            return {int(i): v for i, v in json.load(f).items()}

    @staticmethod
    def get_minos():
        with open(base_config.CONF_PATH / "minos.json", "rt") as f:
            return {int(i): np.array(v) for i, v in json.load(f).items()}
