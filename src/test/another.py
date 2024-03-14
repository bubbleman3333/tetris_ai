import pickle
from src.confs import base_config

s = pickle.load(open(r"C:\Users\aiueo\tetris_ai\src\ai\genetic_algorithm\test2.pickle", "rb"))

path = base_config.CONF_PATH / "populations2.pickle"

pickle.dump(s[:5], open(path, "wb"))
