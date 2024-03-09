import traceback

import numpy as np
import time

from src.ai.tetris_ai.loader import TetrisConfLoader
from src.tools import common


class TetrisPreprocessor:
    def __init__(self):
        self.height = 20
        self.width = 10

        loader = TetrisConfLoader()
        self.hole_height_dic = loader.load_hole_num_dic()
        self.deleted_board = None
        pass

    def calculate_col_height(self, array) -> np.array:
        """
        各行の高さを求める、ただし一番高さが低い行は除く
        :param array:
        :return:
        9次元array
        """
        p = np.argmax(array, axis=0)
        p[np.max(array, axis=0) == 0] = self.height
        p = self.height - p
        return np.delete(p, np.argmin(p))

    def calc_hole_num(self, board) -> int:
        """
        穴の数をカウントする
        :param board:
        :return:
        穴の数の合計
        """
        # 　穴の数をカウントする
        col_to_bytes = [common.hash_array(arr) for arr in board.T]
        hole_num = sum([self.hole_height_dic[col] for col in col_to_bytes])

        print(f"穴の数:{hole_num}")

        return hole_num

    @staticmethod
    def calc_height_std(height) -> np.float64:
        """
        高さの分散を求める。バラつきが少ないほど良いことを学習するという願いを込めて

        :param height: 一番低い高さが削除された9次元配列
        :return: 高さの分散
        """
        return np.var(height) + 0.001

    @staticmethod
    def calc_average_diff(height):
        """
        隣と比較した際のぼこぼこ具合
        :param height:
        :return:
        隣との高さの差の平均
        """
        return abs(np.diff(height)).mean()

    def calc_delete_lines(self, array) -> int:
        """
        削除される行数を計算する
        """
        temp = array[np.any(array == 0, axis=1)]
        deleted_lines = self.height - temp.shape[0]
        if deleted_lines > 0:
            self.deleted_board = np.concatenate((np.zeros((deleted_lines, self.width)).astype(int), temp))
        else:
            self.deleted_board = array
        return deleted_lines

    def calc_horizon_nums_and_invalid_rows(self, board) -> np.array:
        # 有効な行を抽出する
        one_located = np.argmax(board, axis=0)
        max_idx = np.max(one_located)
        temp_board = board[:max_idx]

        # 有効な行の中で横がどのくらい埋まっているかを抽出する
        horizon_sums = np.sum(temp_board, axis=1)
        temp = np.zeros(11)
        idx, val = np.unique(horizon_sums, return_counts=True)
        temp[idx] = val

        # 無効な行数を求める
        invalid_row_num = self.height - max_idx

        return temp / 20, invalid_row_num

    def make_input(self, board):
        """
        機械学習に渡す用のinputを作成する
        ①削除行数、主に報酬として扱ってくれることを願う、多いほどいい
        ②穴の数、少ないほどいい
        ③高さの分散、少ないほどいい
        ④隣との高さの差の平均、基本的には少なければ少ないほどいい
        ⑤高さの最大値
        ⑥高さの最小値
        ⑦高さの平均
        """
        deleted_lines = self.calc_delete_lines(board)
        height = self.calculate_col_height(self.deleted_board)
        valid_row, invalid_row_num = self.calc_horizon_nums_and_invalid_rows(self.deleted_board)
        temp = np.array([
            deleted_lines * 5,  # 削除数は最大で4のため1/4でスケーリングする
            self.calc_hole_num(self.deleted_board) * 0.1,  # 穴の数は最大で200のため、1/200でスケーリングする
            self.calc_height_std(height),
            self.calc_average_diff(height),
            0.99 if height.max() > 12 else 0.01,
            invalid_row_num
        ]) / 20
        return np.concatenate((temp, valid_row))
