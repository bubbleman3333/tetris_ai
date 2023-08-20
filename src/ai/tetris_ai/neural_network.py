import numpy as np


class NeuralNetWork:
    def __init__(self, input_num, middle_num, middle_weight, output_weight):
        self.input_num = input_num
        self.middle_num = middle_num


class Affine:
    def __init__(self, w, b):
        self.w = w
        self.b = b
        self.x = None
        self.dw = None
        self.db = None

    def forward(self, x):
        self.x = x
        out = np.dot(x, self.w) + self.b

        return out

    def backward(self, d_out):
        dx = np.dot(d_out, self.w.T)
        self.dw = np.dot(self.x.T, d_out)
        self.db = np.sum(d_out, axis=0)

        return dx


class Relu:
    def __init__(self):
        self.mask = None

    def forward(self, x):
        self.mask = (x <= 0)
        out = x.copy()
        out[self.mask] = 0
        return out

    def backward(self, d_out):
        d_out[self.mask] = 0
        return d_out
