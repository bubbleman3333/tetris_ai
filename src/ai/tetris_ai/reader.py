import numpy as np
from src.ai.boards.agent_for_show import TetrisAgent
from src.agent.conf_loader import TetrisConfLoader


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
        self.start = np.array([[0], [2]])

    def read(self, board_agent: TetrisAgent):
        return

    def drop_board(self, board: np.array, new_position) -> np.array:
        # 落とし切った盤面を返す
        while True:
            new_position += self.down
            if not self.locatable(new_position, board):
                new_position -= self.down
                break
        return self.locate(new_position=new_position, board=board)

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
        # if self.now_piece.piece_number == 5:
        #     return
        located_position = np.dot(rotate_matrix, position)
        new_position = located_position + center
        return self.locatable_for_rotate(new_position=new_position, board=board)

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
            if not np.all(board[y, x] == 0):
                return new_position

    @staticmethod
    def adjust_start_position(new_position):
        while new_position[1].min() > 0:
            new_position[1] -= 1


p = TetrisBoardReader()

col = p.minos[7] + np.array([[0], [6]])
board = np.zeros((20, 10))
import time

start = time.time()

col = p.rotate_right(board, col, np.array([[0],[0]]))
temp = p.adjust_start_position(col)
col = p.rotate_right(board, col, np.array([[0],[0]]))
temp = p.adjust_start_position(col)
col = p.rotate_right(board, col, np.array([[0],[0]]))
temp = p.adjust_start_position(col)
col = p.rotate_right(board, col, np.array([[0],[0]]))
temp = p.adjust_start_position(col)

p.drop_board(board, col)
print(time.time() - start)
