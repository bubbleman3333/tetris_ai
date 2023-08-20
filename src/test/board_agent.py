import numpy as np
from src.agent.conf_loader import TetrisConfLoader


class TetrisAgent:
    def __init__(self):
        self.board_height = 20
        self.board_width = 10
        self.upper_blank = 3
        self.board = np.zeros((self.board_height + self.upper_blank, self.board_width))
        self.piece_num = 7
        self.now_piece = None
        self.now_position = None
        self.end = False
        loader = TetrisConfLoader()
        self.piece_color = {
            0: "#ffffff",
            1: "#ffa500",
            2: "#0000ff",
            3: "#ffff00",
            4: "#800080",
            5: "#ff0000",
            6: "#00ff00",
            7: "#00ffff"
        }
        self.pieces = {
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

    @staticmethod
    def rotate_right(piece):
        return np.rot90(piece, k=3)

    @staticmethod
    def rotate_left(piece):
        return np.rot90(piece, k=1)

    def move_down(self, piece_pos):
        self.board[self.board < 0] = 0
        piece_pos[:, 0] += 1

    def select_random_block(self):
        return self.pieces[np.random.randint(1, self.piece_num + 1)]

    def move_able(self):
        return

    def rotate_able(self):
        return

    def set_random_block(self):
        self.now_piece = self.select_random_block()
