import tkinter as tk
from src.ai.boards.agent_for_show import TetrisAgent
from src.ai.tetris_ai.ai_main import TetrisAI
from src.ai.controller.move_controller import MoveController


class TetrisPlayForAi:
    def __init__(self):
        self.root = None
        self.root_size = 1000
        self.board_canvas = None
        self.hold_canvas = None
        self.next_block_canvas = None
        self.tetris_frame = None
        self.tetris_agent = TetrisAgent()
        self.rec_size = 40
        self.side_rec_size = self.rec_size * 0.6
        self.side_canvas_length = 5
        self.tetris_frame_width = self.rec_size * (self.tetris_agent.board_width + self.side_canvas_length * 2)
        self.canvas_height = self.rec_size * self.tetris_agent.board_height + 20
        self.canvas_width = self.rec_size * self.tetris_agent.board_width + 20
        self.side_canvas_width = self.side_rec_size * self.side_canvas_length
        self.board_rectangle_dic = {}
        self.hold_rectangle_dic = {}
        self.next_block_rectangle_dic = {}
        self.white = self.tetris_agent.piece_color[0]
        self.highlight_color = self.tetris_agent.piece_color[8]
        self.set_root()
        self.tetris_ai = TetrisAI()
        self.move_controller = MoveController()
        pass

    def set_root(self):
        self.root = tk.Tk()
        self.root.resizable(height=False, width=False)
        self.root.title("Tetris")
        self.root.geometry(f"{self.root_size}x{self.root_size}")
        self.tetris_frame = tk.Frame(self.root, height=self.canvas_height, width=self.tetris_frame_width)
        self.board_canvas = tk.Canvas(self.tetris_frame, width=self.canvas_width, height=self.canvas_height,
                                      background="white",
                                      )
        self.hold_canvas = tk.Canvas(self.tetris_frame, width=self.side_canvas_width, height=self.canvas_height,
                                     background="white",
                                     )
        self.next_block_canvas = tk.Canvas(self.tetris_frame, width=self.side_canvas_width, height=self.canvas_height,
                                           background="white",
                                           )
        self.tetris_frame.pack()
        self.hold_canvas.pack(side="left")
        self.board_canvas.pack(side="left")
        self.next_block_canvas.pack(side="left")
        self.create_board()
        self.create_side(True)
        self.create_side(False)

    def agent_play(self):
        self.reset()
        if self.move_controller.move_end:
            move_list = self.tetris_ai.choice(self.tetris_agent)
            self.move_controller.set_move(move_list)
        if self.tetris_agent.agent_move(self.move_controller.move()):
            self.draw_board()
        self.root.after(100, self.agent_play)
        self.tetris_agent.update_success = False

    def reset(self):
        if self.tetris_agent.end:
            self.tetris_agent.reset()
            self.draw_board()
            self.tetris_agent.set_random_block()
            self.draw_board()

    def move_down(self):
        self.reset()
        if self.tetris_agent.move_down():
            self.draw_board()
        self.root.after(700, self.move_down)

    def move_left(self):
        if self.tetris_agent.move_left():
            self.draw_board()

    def move_right(self):
        if self.tetris_agent.move_right():
            self.draw_board()

    def rotate_left(self):
        if self.tetris_agent.rotate_left():
            self.draw_board()

    def rotate_right(self):
        if self.tetris_agent.rotate_right():
            self.draw_board()

    def play(self):
        self.tetris_agent.set_random_block()
        # self.root.after(0, self.move_down)
        self.root.after(0, self.agent_play())
        self.root.mainloop()

    def change_color(self, key, color):
        self.board_canvas.itemconfig(self.board_rectangle_dic[key], fill=color)

    def change_side_piece_color(self, key, color, outline, next_piece=True):
        canvas = self.next_block_canvas if next_piece else self.hold_canvas
        dic = self.next_block_rectangle_dic if next_piece else self.hold_rectangle_dic
        canvas.itemconfig(dic[key], fill=color, outline=outline)

    def draw_board(self):
        if self.tetris_agent.next_block_changed:
            self.draw_next_block()
        if self.tetris_agent.hold_block_changed:
            self.draw_hold()
        if self.tetris_agent.highlight_change:
            self.draw_highlight()
        if self.tetris_agent.update_success:
            y, x = self.tetris_agent.update_pos
            for s, t in zip(y, x):
                key = (s, t)
                if key in self.board_rectangle_dic:
                    self.change_color(key, self.tetris_agent.piece_color[abs(self.tetris_agent.board[s, t])])
            return
        for h in range(self.tetris_agent.board_height):
            for w in range(self.tetris_agent.board_width):
                key = (h, w)
                self.change_color(key, self.tetris_agent.piece_color[abs(self.tetris_agent.board[h, w])])

    def create_board(self):
        for h in range(self.tetris_agent.board_height):
            for w in range(self.tetris_agent.board_width):
                key = (h, w)
                self.board_rectangle_dic[key] = self.board_canvas.create_rectangle(
                    w * self.rec_size,
                    h * self.rec_size,
                    (w + 1) * self.rec_size,
                    (h + 1) * self.rec_size,
                    fill=self.tetris_agent.piece_color[abs(self.tetris_agent.board[h, w])],
                    outline="black",
                    width=1
                )

    def create_side(self, hold=True):
        canvas = self.hold_canvas if hold else self.next_block_canvas
        dic = self.hold_rectangle_dic if hold else self.next_block_rectangle_dic
        canvas.create_rectangle(
            0,
            0,
            self.side_canvas_length * self.side_rec_size,
            self.side_canvas_length * self.side_rec_size,
            fill=self.white,
            outline="black",
            width=1
        )
        for h in range(self.side_canvas_length):
            for w in range(self.side_canvas_length):
                key = (h, w)
                dic[key] = canvas.create_rectangle(
                    w * self.side_rec_size,
                    h * self.side_rec_size,
                    (w + 1) * self.side_rec_size,
                    (h + 1) * self.side_rec_size,
                    outline="",
                    fill=self.white,
                )

    def draw_next_block(self):
        if self.tetris_agent.deleted_next_mino is not None:
            y, x = self.tetris_agent.deleted_next_mino
            for s, t in zip(y, x):
                self.change_side_piece_color((s, t), self.white, outline="")
        y, x = self.tetris_agent.next_piece.position + self.tetris_agent.next_block_center
        for s, t in zip(y, x):
            self.change_side_piece_color((s, t),
                                         self.tetris_agent.piece_color[self.tetris_agent.next_piece.piece_number],
                                         outline="black"
                                         )
        self.tetris_agent.next_block_changed = False

    def draw_hold(self):
        if self.tetris_agent.deleted_hold_mino is not None:
            y, x = self.tetris_agent.deleted_hold_mino
            for s, t in zip(y, x):
                self.change_side_piece_color((s, t), self.white, next_piece=False, outline="")
        y, x = self.tetris_agent.hold_piece.position + self.tetris_agent.next_block_center
        for s, t in zip(y, x):
            self.change_side_piece_color((s, t),
                                         self.tetris_agent.piece_color[self.tetris_agent.hold_piece.piece_number],
                                         next_piece=False, outline="black")
        self.tetris_agent.hold_block_changed = False

    def draw_highlight(self):
        if self.tetris_agent.highlight_deleted is not None:
            y, x = self.tetris_agent.highlight_deleted
            for s, t in zip(y, x):
                self.change_color((s, t), self.white)
        y, x = self.tetris_agent.highlight_positions
        for s, t in zip(y, x):
            if s >= 3:
                self.change_color((s, t), self.highlight_color)
        self.tetris_agent.highlight_change = False

    def hold(self):
        if self.tetris_agent.hold():
            self.draw_board()
        return

    def drop(self):
        self.tetris_agent.drop()
        self.tetris_agent.set_random_block()

    def key_pressed(self, event):
        code = event.keycode
        print(code)
        if code == 37:
            self.move_left()
        elif code == 38:
            self.drop()
        elif code == 39:
            self.move_right()
        elif code == 40:
            self.move_down()
        elif code == 65:
            self.rotate_left()
        elif code == 68:
            self.rotate_right()
        elif code == 83:
            self.hold()


agent = TetrisPlayForAi()
agent.play()
