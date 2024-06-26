import numpy as np
from src.confs import base_config


class NeuralNetWork:
    def __init__(self, input_num, middle_num, load_params=True, file_name="", lr=0.3):
        self.input_num = input_num
        self.middle_num = middle_num
        self.lr = lr
        self.file_name = file_name
        if load_params:
            mw, mb, ow, ob = self.load_param()
        else:
            mw = np.random.rand(self.input_num, self.middle_num) - 0.5
            mb = np.random.rand(self.middle_num) - 0.5
            ow = np.random.rand(self.middle_num, 1) - 0.5
            ob = np.random.rand() - 0.5
        self.middle_affine = Affine(mw, mb)
        self.output_affine = Affine(ow, ob)
        self.layers = [self.middle_affine, Relu(), self.output_affine]
        self.params = [self.middle_affine, self.output_affine]
        self.last_layer = MeanSquaredError()
        self.loss_list = []
        self.t = 0

    def forward(self, input_, target=None):
        for layer in self.layers:
            input_ = layer.forward(input_)
        if target is not None:
            self.loss(input_, target)
        return input_

    def loss(self, out, target):
        t = self.last_layer.forward(out, target)
        self.loss_list.append(t)

    def backward(self):
        d_loss = self.last_layer.backward()
        for layer in self.layers[::-1]:
            d_loss = layer.backward(d_loss)

    def update(self):
        for layer in self.params:
            layer.w -= self.lr * layer.dw
            layer.b -= self.lr * layer.db

    def train(self, input_, target_):
        self.forward(input_, target_)
        self.backward()
        self.update()
        self.t += 1
        if self.t % 100 == 0:
            self.save()
            print("saved")

    def save(self):
        param_dir = base_config.PARAM_PATH
        np.save(param_dir / f"middle_w{self.file_name}", self.middle_affine.w)
        np.save(param_dir / f"middle_b{self.file_name}", self.middle_affine.b)
        np.save(param_dir / f"output_w{self.file_name}", self.output_affine.w)
        np.save(param_dir / f"output_b{self.file_name}", self.output_affine.b)

    def load_param(self):
        param_dir = base_config.PARAM_PATH
        middle_w = np.load(param_dir / f"middle_w{self.file_name}.npy")
        middle_b = np.load(param_dir / f"middle_b{self.file_name}.npy")
        output_w = np.load(param_dir / f"output_w{self.file_name}.npy")
        output_b = np.load(param_dir / f"output_b{self.file_name}.npy")
        print("weight loaded")
        return middle_w, middle_b, output_w, output_b


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

# nn = NeuralNetWork(10, 100)
# num_target = 10
# x = np.random.rand(16, 10)
# t = np.arange(-5, 1 + num_target).reshape((16, 1))
# for i in range(100):
#     nn.train(x, t)
#
# # print(nn.forward(x))
# # import matplotlib.pyplot as plt
# #
# # plt.plot(np.arange(len(nn.loss_list)),nn.loss_list)
# # plt.show()
#
# print(nn.forward(x))
