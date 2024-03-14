import numpy as np
from src.confs import base_config


class NeuralNetWorkByGenetic:
    def __init__(self, mw, mb, ow, ob):
        self.middle_affine = Affine(mw, mb)
        self.output_affine = Affine(ow, ob)
        self.layers = [self.middle_affine, Relu(), self.output_affine]
        self.params = [self.middle_affine, self.output_affine]
        self.last_layer = MeanSquaredError()
        self.loss_list = []
        self.t = 0

    def forward(self, input_):
        for layer in self.layers:
            input_ = layer.forward(input_)
        return input_


class Affine:
    def __init__(self, w, b):
        self.w = w
        self.b = b
        self.x = None
        self.dw = None
        self.db = None
        self.batch_size = None

    def forward(self, x):
        self.x = x
        out = np.dot(x, self.w) + self.b
        self.batch_size = x[0].shape

        return out

    def backward(self, d_out):
        dx = np.dot(d_out, self.w.T)
        self.dw = np.dot(self.x.T, d_out) / self.batch_size  # バッチサイズで割る
        self.db = np.sum(d_out, axis=0) / self.batch_size  # バッチサイズで割る

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


class MeanSquaredError:
    def __init__(self):
        self.y = None  # 真の値
        self.t = None  # 教師データ

    def forward(self, y, t):
        self.y = y.reshape((t.shape[0], 1))
        self.t = t
        loss = 0.5 * np.sum((y - t) ** 2)
        return loss

    def backward(self):
        d_loss = self.y - self.t
        return d_loss
