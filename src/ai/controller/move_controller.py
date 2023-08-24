from src.ai.controller.method_controller import MethodController
from src.ai.boards.agent_for_show import TetrisAgent


class MoveController:
    def __init__(self):
        self.move_list = None
        self.method_controller = MethodController()
        self.now_phase = 0
        self.phase_dict = {}
        self.now_rotate = None

    def set_move(self, move_list):
        self.move_list = move_list

    def move(self, agent: TetrisAgent):
        return self.phase_dict[self.now_phase](agent)

    def phase1(self, agent=None):
        self.now_phase += 1
        if self.move_list[0]:
            return self.method_controller.hold
        else:
            return self.phase2

