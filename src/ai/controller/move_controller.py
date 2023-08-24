from src.ai.controller.method_controller import MethodController
from src.ai.boards.agent_for_show import TetrisAgent


class MoveController:
    def __init__(self):
        self.move_list = None
        self.method_controller = MethodController()
        self.move_limit = None
        self.move_num = 0
        self.move_end = True

    def set_move(self, move_list):
        self.move_list = []
        '''
        move_list概要
        0:holdするか否か
        1:何回回転するか
        2:どのくらい横移動するか
        3:ドロップをしない場合何回下に動かすか
        4:ドロップをしない場合、最下点から左右にどのくらい動かすか
        '''
        if move_list[0]:
            self.move_list.append(self.method_controller.hold)
        num_rotate = move_list[1]
        self.move_list += [self.method_controller.rotate_right] * num_rotate
        move_num = move_list[2]
        if move_num < 0:
            self.move_list += abs(move_num) * [self.method_controller.move_left]
        else:
            self.move_list += move_num * [self.method_controller.move_right]
        if move_list[3] is not None:
            self.move_list += move_list[3] * [self.method_controller.move_down]
            move_num = move_list[4]
            if move_num < 0:
                self.move_list += abs(move_num) * [self.method_controller.move_left]
            else:
                self.move_list += move_num * [self.method_controller.move_right]
        else:
            self.move_list.append(self.method_controller.drop)

        self.move_limit = len(self.move_list)
        self.move_end = False
        self.move_num = 0

    def move(self):
        num = self.move_list[self.move_num]
        self.move_num += 1
        if self.move_num >= self.move_limit:
            self.move_end = True
        return num
