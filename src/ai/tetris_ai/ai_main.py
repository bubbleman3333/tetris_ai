from src.ai.tetris_ai.reader import TetrisBoardReader
from src.ai.tetris_ai.neural_network import NeuralNetWork
from src.ai.tetris_ai.preprocessor import TetrisPreprocessor
from src.ai.boards.agent_for_show import TetrisAgent
import numpy as np


class TetrisAI:
    def __init__(self):
        self.reader = TetrisBoardReader()
        self.neural_net = NeuralNetWork(input_num=18, middle_num=50)
        self.input_ = None
        self.scores = None
        self.arg_max = None
        self.processor = TetrisPreprocessor()
        self.board_list = None
        self.origin_board_input = None
        self.gamma = 0.98

    def make_input(self, agent: TetrisAgent):
        board = agent.board.copy()
        board[board > 0] = 1
        board[board <= 0] = 0
        self.origin_board_input = np.array([self.processor.make_input(board)])
        self.board_list = self.reader.read(agent)
        input_ = np.array([self.processor.make_input(board) for board in self.board_list])
        return input_

    def predict(self, agent: TetrisAgent):
        self.input_ = self.make_input(agent)
        return self.neural_net.forward(self.input_)

    def choice(self, agent: TetrisAgent):
        self.scores = self.predict(agent)
        self.arg_max = self.scores.argmax()
        return self.reader.state.history[self.arg_max]

    def train(self, r):
        now_score = self.neural_net.forward(self.origin_board_input)
        next_score = self.scores[self.arg_max]
        new_score = now_score + self.neural_net.lr * (r + self.gamma * next_score - now_score)
        target = np.array([new_score]).reshape((1, 1))
        self.neural_net.train(np.array(self.origin_board_input), target)

# age = TetrisAgent()
#
# age.set_random_block()
#
# ai = TetrisAI()
# import time
#
# start = time.time()
#
# # answer = ai.predict(agent=age)
# # print(answer)
# # print(answer.argmax())
# # print(max(answer))
# print(ai.choice(agent=age))
# print(time.time() - start)
