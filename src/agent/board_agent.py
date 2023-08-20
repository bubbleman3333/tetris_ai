import numpy as np
from typing import Union
from src.agent.conf_loader import TetrisConfLoader


class TetrisAgent:
    def __init__(self):
        self.board_height = 20
        self.board_width = 10
        self.board = np.zeros((self.board_height, self.board_width)).astype(int)
        self.piece_num = 7
        self.now_piece: Union[Piece, None] = None
        self.next_piece: Union[Piece, None] = None
        self.hold_piece: Union[Piece, None] = None

        self.end = False
        loader = TetrisConfLoader()
        self.piece_color = loader.get_piece_color_dict()
        self.minos = loader.get_minos()
        self.first_position = np.array([[0], [4]])
        self.down = np.array([[1], [0]])
        self.right = np.array([[0], [1]])
        self.left = np.array([[0], [-1]])
        self.no_move = np.array([[0], [0]])
        self.rotate_left_matrix = np.array([[0, -1], [1, 0]])
        self.rotate_right_matrix = np.array([[0, 1], [-1, 0]])
        self.next_block_center = np.array([[2], [2]])

        self.update_pos = None
        self.update_success = False

        self.remain = list(range(1, 8))
        self.next_block_changed = False
        self.deleted_next_mino = None

        self.hold_block_changed = False
        self.deleted_hold_mino = None

        self.hold_able = True

        self.highlight_change = False
        self.highlight_positions = None
        self.highlight_deleted = None
        self.method_list = [self.rotate_left, self.rotate_right, self.move_left, self.move_down, self.move_right,
                            self.hold, self.drop]

    def reset(self):
        self.next_block_changed = False
        self.deleted_next_mino = None

        self.hold_block_changed = False
        self.deleted_hold_mino = None

        self.hold_able = True

        self.highlight_change = False
        self.highlight_positions = None
        self.highlight_deleted = None
        self.update_pos = None
        self.update_success = False

        self.remain = list(range(1, 8))
        self.next_block_changed = False
        self.deleted_next_mino = None
        self.end = False

        self.board = np.zeros((self.board_height, self.board_width))

    def rotate(self, rotate_matrix):
        if self.now_piece.piece_number == 5:
            self.update_pos = None
            self.update_success = False
            return False
        located_position = np.dot(rotate_matrix, self.now_piece.position)
        new_position = located_position + self.now_piece.center
        can_rotate, new_position, move = self.locatable_for_rotate(new_position)
        if not can_rotate:
            self.update_pos = None
            self.update_success = False
            return False
        self.locate(self.now_piece.position + self.now_piece.center, new_position, -1)
        self.now_piece.position = located_position
        self.now_piece.center += move
        self.make_highlight()
        return True

    def rotate_right(self):
        return self.rotate(self.rotate_left_matrix)

    def rotate_left(self):
        return self.rotate(self.rotate_right_matrix)

    def move_down(self):
        if not self.move(self.down, highlight=False):
            y, x = self.now_piece.position + self.now_piece.center
            self.board[y, x] = self.now_piece.piece_number
            result = self.delete_line()
            self.set_random_block()
            self.hold_able = True
            if result:
                self.update_pos = None
                self.update_success = False
        return True

    def move_left(self):
        if self.move(self.left):
            return True

    def move_right(self):
        if self.move(self.right):
            return True

    def select_random_number(self):
        if len(self.remain) == 0:
            self.remain = list(range(1, 8))
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
        if y.max() >= self.board_height or x.max() >= self.board_width:
            return False
        if self.board[y, x].max() > 0:
            return False
        return True

    def locatable_for_rotate(self, new_position):
        y, x = new_position
        y_min, y_max, x_min, x_max = y.min(), y.max(), x.min(), x.max()
        if y_max >= self.board_height:
            return False, None, None
        if y_min <= -1:
            update = self.down * abs(y_min)
            temp_position = new_position + update
            if self.locatable(temp_position):
                return True, temp_position, update
            else:
                return False, None, None
        elif x_max >= self.board_width:
            update = self.left * (x_max - self.board_width + 1)
            temp_position = new_position + update
            if self.locatable(temp_position):
                return True, temp_position, update
            else:
                return False, None, None
        elif x_min <= -1:
            update = self.right * abs(x_min)
            temp_position = new_position + update
            if self.locatable(temp_position):
                return True, temp_position, update
            else:
                return False, None, None
        else:
            if self.board[y, x].max() > 0:
                return False, None, None
            return True, new_position, self.no_move

    def locate(self, old_position, new_position, num):
        y, x = old_position
        self.board[y, x] = 0
        y, x = new_position
        self.board[y, x] = self.now_piece.piece_number * num
        if self.update_success:
            self.update_pos = np.concatenate((self.update_pos, old_position, new_position), axis=1).tolist()
        else:
            self.update_pos = np.concatenate((old_position, new_position), axis=1).tolist()

        self.update_success = True

    def move(self, move_num: np.ndarray, highlight=True, deleted_highlight=True):
        temp = self.now_piece.center + move_num
        new_position = self.now_piece.position + temp
        if not self.locatable(new_position):
            self.update_pos = None
            self.update_success = False
            return False
        now_position = self.now_piece.center + self.now_piece.position
        self.locate(now_position, new_position, -1)
        self.now_piece.center = temp
        if highlight:
            self.make_highlight(deleted_highlight)
        return True

    def set_random_block(self):
        del self.now_piece
        if self.next_piece is not None:
            self.deleted_next_mino = self.next_block_center + self.next_piece.position
            self.now_piece = self.next_piece
        else:
            self.now_piece = self.select_piece()
        self.next_block_changed = True
        self.next_piece = self.select_piece()

        if not self.move(self.no_move, deleted_highlight=False):
            self.end = True

    def hold(self):
        if not self.hold_able:
            return False
        old_position = self.now_piece.center + self.now_piece.position
        if self.hold_piece is None:
            self.hold_piece = self.select_piece(self.now_piece.piece_number)
            self.now_piece = self.next_piece
            self.deleted_next_mino = self.next_block_center + self.next_piece.position
            self.next_block_changed = True
            self.next_piece = self.select_piece()
        else:
            temp = self.now_piece
            self.now_piece = self.select_piece(self.hold_piece.piece_number)
            self.deleted_hold_mino = self.next_block_center + self.hold_piece.position
            self.hold_piece = self.select_piece(temp.piece_number)
        self.make_highlight()
        self.locate(old_position, self.now_piece.center + self.now_piece.position, -1)
        self.hold_block_changed = True
        self.hold_able = False
        return True

    def drop(self):
        origin_position = self.now_piece.center + self.now_piece.position
        self.locate(origin_position, self.highlight_positions, 1)
        self.delete_line()
        self.hold_able = True
        return True

    def delete_line(self, from_hold=False):
        temp = self.board[np.any(self.board == 0, axis=1)]
        if temp.shape[0] != self.board_height:
            self.board = np.concatenate(
                (np.zeros((self.board_height - temp.shape[0], self.board_width)),
                 temp), axis=0)
            if not from_hold:
                self.update_pos = None
                self.update_success = False
            return True
        return False

    def make_highlight(self, deleted_update=True):
        new_position = self.now_piece.center + self.now_piece.position
        while True:
            new_position += self.down
            if not self.locatable(new_position):
                new_position -= self.down
                break
        self.highlight_deleted = self.highlight_positions if deleted_update else None
        self.highlight_positions = new_position
        self.highlight_change = True


class Piece:
    def __init__(self, center, piece_number, position):
        self.center = center
        self.piece_number = piece_number
        self.position = position
