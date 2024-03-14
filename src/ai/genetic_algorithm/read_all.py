from src.agent.conf_loader import TetrisConfLoader
import numpy as np
from src.ai.genetic_algorithm.reader_for_genetic import TetrisBoardReader
from src.ai.genetic_algorithm.neural_netword_for_genetic import NeuralNetWork
from src.ai.tetris_ai.preprocessor import TetrisPreprocessor

loader = TetrisConfLoader()

minos = loader.get_minos()
PIECE_NUMS = 400


# 指定した分のピースを集める。

def get_pieces():
    pieces = []
    remain = list(range(1, 8))

    while len(pieces) < PIECE_NUMS:
        if not len(remain):
            remain = list(range(1, 8))
        num = remain.pop(np.random.randint(len(remain)))
        pieces.append(num)
    return pieces


processor = TetrisPreprocessor()
reader = TetrisBoardReader()


def delete_board(array):
    """
    削除される行数を計算する
    """
    temp = array[np.any(array == 0, axis=1)]
    deleted_lines = 20 - temp.shape[0]
    if deleted_lines > 0:
        deleted_board = np.concatenate((np.zeros((deleted_lines, 10)).astype(int), temp))
    else:
        deleted_board = array
    return deleted_board, deleted_lines * 10


def play(pieces, neural_network: NeuralNetWork):
    board = np.zeros((20, 10)).astype(int)
    score = 0
    for idx, i in enumerate(pieces):
        score += 1
        position = minos[i]
        board_list = reader.read(board, position=position, piece_number=i)
        if len(board_list) == 0:
            break
        input_ = np.array([processor.make_input(b) for b in board_list])
        score_list = neural_network.forward(input_)
        board = board_list[score_list.argmax(axis=0)[0]]
        board, delete_score = delete_board(board)
        # score += delete_score
    return score
