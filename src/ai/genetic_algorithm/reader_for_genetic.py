import numpy as np
from src.ai.boards.agent_for_show import TetrisAgent
from src.agent.conf_loader import TetrisConfLoader
from src.tools.common import hash_array


class TetrisBoardReader:
    def __init__(self):
        self.down = np.array([[1], [0]])
        self.right = np.array([[0], [1]])
        self.left = np.array([[0], [-1]])
        self.no_move = np.array([[0], [0]])
        self.board_height = 20
        self.board_width = 10
        self.rotate_left_matrix = np.array([[0, -1], [1, 0]])
        self.rotate_right_matrix = np.array([[0, 1], [-1, 0]])
        loader = TetrisConfLoader()
        self.minos = loader.get_minos()
        self.start = np.array([[0], [4]])
        self.state = State()
        self.piece_state = PieceState()

    def reset(self):
        self.state.reset()

    def read(self, board: np.array, piece_number,position ):
        self.reset()
        position = position.copy()
        board = board.copy()
        board[board > 0] = 1
        board[board < 0] = 0
        board_list = self.__read_of_piece(board, position, piece_number)
        return board_list

    def __read_of_piece(self, board, position, piece_number):
        board_list = []

        if piece_number == 2:
            num_rotate = 2
        elif piece_number == 5:
            num_rotate = 1
        else:
            num_rotate = 4

        new_position = position + self.start
        for i in range(num_rotate):
            self.piece_state.num_rotate = i
            y, x = new_position
            self.piece_state.num_drop = 19 - y.max()
            for direction in (-1, 1):
                if direction == -1:
                    start_position, end_position = -1, -x.min() - 1,
                else:
                    start_position, end_position = 0, 10 - x.max(),
                for moves in range(start_position, end_position, direction):
                    move_position = new_position + self.right * moves
                    if not self.locatable(new_position=move_position, board=board):
                        break
                    self.piece_state.num_move = moves
                    board_list += self.drop_board(board=board, origin_position=move_position)
            if i == num_rotate - 1:
                break
            new_position, position = self.rotate_right(position=position, board=board, center=self.start)
            if new_position is None:
                break
        return board_list

    def get_drop_position(self, board, new_position):

        while True:
            new_position += self.down
            if not self.locatable(new_position, board):
                new_position -= self.down
                break
        return new_position

    @staticmethod
    def has_upper_block(board, position, left):
        y, x = position
        if y.min() == 0:
            return False
        temp = x.min() if left else x.max()
        return board[y[x == temp].min() - 1, temp] > 0

    def drop_board(self, board: np.array, origin_position) -> np.array:
        # 落とし切った盤面を返す、落とし切った後左右に動かせる場合はそれも渡す、返却はリスト
        return_array = []

        def move_and_add_hash(left):
            board_copy = board.copy()
            move = self.left if left else self.right
            for i in range(1, 3):
                move_position = new_position + move * i
                if not self.locatable(move_position, board_copy):
                    break
                if not self.has_upper_block(board=board_copy, position=move_position, left=left):
                    break
                hash_arr = hash_array(move_position)
                if hash_arr in self.state.seen:
                    break
                self.state.seen.add(hash_arr)
                self.state.history.append(
                    (self.state.hold, self.piece_state.num_rotate, self.piece_state.num_move,
                     self.piece_state.num_drop, move[1][0] * i))
                y, x = origin_position
                board_copy[y, x] = 1
                return_array.append(self.locate(new_position=move_position, board=board))

        new_position = self.get_drop_position(board=board, new_position=origin_position.copy())
        origin_hash = hash_array(new_position)
        if origin_hash not in self.state.seen:
            self.state.seen.add(origin_hash)
            # 盤面操作用の状態管理
            self.state.history.append(
                (self.state.hold, self.piece_state.num_rotate, self.piece_state.num_move, None, None))
            return_array.append(self.locate(new_position=new_position, board=board))
        move_and_add_hash(True)
        move_and_add_hash(False)
        return return_array

    def locatable(self, new_position, board):
        if new_position.min() < 0:
            return False
        y, x = new_position
        if y.max() >= self.board_height or x.max() >= self.board_width:
            return False
        return np.all(board[y, x] == 0)

    @staticmethod
    def locate(new_position, board):
        cop = board.copy()
        y, x = new_position
        cop[y, x] = 1
        return cop

    def rotate(self, rotate_matrix, board, position, center):
        """
        回転した場合のポジションのみを返す
        :param rotate_matrix:
        :param board:
        :param position:
        :param center:
        :return:
        """
        located_position = np.dot(rotate_matrix, position)
        new_position = located_position + center
        return self.locatable_for_rotate(new_position=new_position, board=board), located_position

    def rotate_right(self, board, position, center):
        return self.rotate(rotate_matrix=self.rotate_left_matrix, board=board, position=position, center=center)

    def locatable_for_rotate(self, new_position, board):
        y, x = new_position
        y_min, y_max, x_min, x_max = y.min(), y.max(), x.min(), x.max()
        if y_max >= self.board_height:
            return False, None, None
        if y_min <= -1:
            update = self.down * abs(y_min)
            temp_position = new_position + update
            if self.locatable(new_position=temp_position, board=board):
                return temp_position
            else:
                return
        elif x_max >= self.board_width:
            update = self.left * (x_max - self.board_width + 1)
            temp_position = new_position + update
            if self.locatable(new_position=temp_position, board=board):
                return temp_position
            else:
                return
        elif x_min <= -1:
            update = self.right * abs(x_min)
            temp_position = new_position + update
            if self.locatable(new_position=temp_position, board=board):
                return temp_position
            else:
                return
        else:
            if np.all(board[y, x] == 0):
                return new_position

    @staticmethod
    def adjust_start_position(new_position):
        while new_position[1].min() > 0:
            new_position[1] -= 1
        return new_position


class State:
    def __init__(self):
        self.seen = set()
        self.history = []
        self.hold = False

    def reset(self):
        self.seen = set()
        self.history = []
        self.hold = False

    def add_history(self, his):
        self.history.append(his)

    def get_history(self):
        return self.history

    def add_seen(self, hash_board):
        self.seen.add(hash_board)


class PieceState:
    def __init__(self):
        self.num_rotate = None
        self.num_move = None
        self.num_drop = None

    def reset(self):
        self.num_rotate = None
        self.num_move = None
        self.num_drop = None

# p = TetrisBoardReader()
#
# col = p.minos[7]
# board = np.zeros((20, 10))
#
# base = np.array([[0], [2]])
# # for i in p.minos.values():
# #     y, x = base + i
# #     b_copy = board.copy()
# #     b_copy[y, x] = 1
# board[np.array([18, 18, 19]), np.array([1, 2, 1])] = 2
# import time
#
# start = time.time()
#
# col = p.rotate_right(board, col, np.array([[5], [5]]))
# temp = p.adjust_start_position(col[0])
#
# c = p.read_of_piece(board=board, position=col[0], piece_number=7)
# print(p.state.history)
# print(len(c))
# for idx, i in enumerate(c):
#     print(i)
#     print(p.state.history[idx])
#     print("=" * 30)
# print(time.time() - start)
