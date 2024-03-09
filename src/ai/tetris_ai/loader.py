from src.confs import base_config
import json


class TetrisConfLoader:
    @staticmethod
    def load_hole_num_dic():
        with open(base_config.CONF_PATH / "test.json", "rt", encoding="utf-8") as f:
            return {bytes.fromhex(i): v for i, v in json.load(f).items()}
