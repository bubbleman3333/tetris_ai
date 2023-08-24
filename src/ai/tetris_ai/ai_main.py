from src.ai.tetris_ai.reader import TetrisBoardReader
from src.ai.tetris_ai.neural_network import NeuralNetWork
from src.ai.tetris_ai.preprocessor import TetrisPreprocessor
from src.ai.boards.agent_for_show import TetrisAgent
import numpy as np


class TetrisAI:
    def __init__(self):
        self.reader = TetrisBoardReader()
        self.neural_net = NeuralNetWork(input_num=18, middle_num=50)
        self.processor = TetrisPreprocessor()

    def make_input(self, agent: TetrisAgent):
        board_list = self.reader.read(agent)
        input_ = np.array([self.processor.make_input(board) for board in board_list])
        return input_

    def predict(self, agent: TetrisAgent):
        input_ = self.make_input(agent)
        return self.neural_net.forward(input_)

    def choice(self, agent: TetrisAgent):
        scores = self.predict(agent)
        return self.reader.state.history[scores.argmax()]



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
