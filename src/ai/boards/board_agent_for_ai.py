import random

import numpy as np
from typing import Union
from src.agent.conf_loader import TetrisConfLoader


class TetrisAgentForAI:
    def __init__(self):
        self.board_height = 20
        self.board_width = 10
        self.upper_blank = 3
        self.board = np.zeros((self.board_height + self.upper_blank, self.board_width)).astype(int)
        self.piece_num = 7
        self.now_piece: Union[Piece, None] = None
        self.next_piece: Union[Piece, None] = None
        self.hold_piece: Union[Piece, None] = None

        self.end = False
        loader = TetrisConfLoader()
        self.minos = loader.get_minos()
        self.first_position = np.array([[3], [4]])
        self.down = np.array([[1], [0]])
        self.right = np.array([[0], [1]])
        self.left = np.array([[0], [-1]])
        self.no_move = np.array([[0], [0]])
        self.rotate_left_matrix = np.array([[0, -1], [1, 0]])
        self.rotate_right_matrix = np.array([[0, 1], [-1, 0]])

        self.remain = list(range(1, 8))

        self.hold_able = True

        self.blank = 0
        self.stone = 1

        self.method_list = [self.rotate_left, self.rotate_right, self.move_left, self.move_down, self.move_right,
                            self.drop]

    def rotate(self, rotate_matrix):
        located_position = np.dot(rotate_matrix, self.now_piece.position)
        new_position = located_position + self.now_piece.center
        if not self.locatable(new_position) or self.now_piece.piece_number == 5:
            return False
        self.locate(self.now_piece.position + self.now_piece.center, new_position, -1)
        self.now_piece.position = located_position
        return True

    def rotate_right(self):
        self.rotate(self.rotate_left_matrix)
        return True

    def rotate_left(self):
        self.rotate(self.rotate_right_matrix)
        return True

    def move_down(self):
        if not self.move(self.down):
            y, x = self.now_piece.position + self.now_piece.center
            self.board[y, x] = self.now_piece.piece_number
            self.delete_line()
            self.set_random_block()
            self.hold_able = True
        return True

    def move_left(self):
        if self.move(self.left):
            return True

    def move_right(self):
        if self.move(self.right):
            return True

    def select_random_number(self):
        if len(self.remain) == 0:
            self.remain = list(range(1, self.piece_num + 1))
        return self.remain.pop(np.random.randint(len(self.remain)))

    def select_piece(self, piece_number=None):
        if piece_number is None:
            piece_number = self.select_random_number()
        piece = Piece(center=self.first_position.copy(), piece_number=piece_number,
                      position=self.minos[piece_number].copy())
        return piece

    def locatable(self, new_position):
        if new_position.min() < 0:
            return False
        y, x = new_position
        if y.max() >= self.board_height + self.upper_blank or x.max() >= self.board_width:
            return False
        if self.board[y, x].max() > 0:
            return False
        return True

    def locate(self, old_position, new_position, num):
        y, x = old_position
        self.board[y, x] = 0
        y, x = new_position
        self.board[y, x] = self.stone * num

    def move(self, move_num: np.ndarray):
        temp = self.now_piece.center + move_num
        new_position = self.now_piece.position + temp
        if not self.locatable(new_position):
            return False
        now_position = self.now_piece.center + self.now_piece.position
        self.locate(now_position, new_position, -1)
        self.now_piece.center = temp
        return True

    def set_random_block(self):
        if self.next_piece is not None:
            self.now_piece = self.next_piece
        else:
            self.now_piece = self.select_piece()
        self.next_piece = self.select_piece()

        if not self.move(self.no_move):
            self.end = True

    def hold(self):
        old_position = self.now_piece.center + self.now_piece.position
        if self.hold_piece is None:
            self.hold_piece = self.select_piece(self.now_piece.piece_number)
            self.now_piece = self.next_piece
            self.next_piece = self.select_piece()
        else:
            temp = self.now_piece
            self.now_piece = self.select_piece(self.hold_piece.piece_number)
            self.hold_piece = self.select_piece(temp.piece_number)
        self.locate(old_position, self.now_piece.center + self.now_piece.position, -1)
        self.hold_able = False

    def drop(self):
        origin_position = self.now_piece.center + self.now_piece.position
        new_position = self.now_piece.center + self.now_piece.position
        while True:
            new_position += self.down
            if not self.locatable(new_position):
                new_position -= self.down
                break
        self.locate(origin_position, new_position, 1)
        self.delete_line()
        self.hold_able = True
        self.set_random_block()

    def delete_line(self):
        temp = self.board[np.any(self.board == 0, axis=1)]
        if temp.shape[0] != self.upper_blank + self.board_height:
            self.board = np.concatenate(
                (np.zeros((self.upper_blank + self.board_height - temp.shape[0], self.board_width)),
                 temp), axis=0)
            return True
        return False

    def random_move(self):
        method = random.choice(self.method_list)
        method()


class Piece:
    def __init__(self, center, piece_number, position):
        self.center = center
        self.piece_number = piece_number
        self.position = position
