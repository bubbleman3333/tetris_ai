import numpy as np

from src.ai.tetris_ai.loader import TetrisConfLoader
from src.tools import common

loader = TetrisConfLoader()
hole_height_dic = loader.load_hole_num_dic()

def calc_hole_num(board:np.array):
    col_to_bytes = [common.hash_array(arr) for arr in board.T]
    hole_num = sum([hole_height_dic[col] for col in col_to_bytes])

    return hole_num


def create_one_or_zero_board(board:np.array,show=False):
    board = board.copy()
    board[board > 0] = 1
    board[board <= 0] = 0
    if show:
        print(board)
    return board

