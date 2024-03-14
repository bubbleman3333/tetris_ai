import concurrent.futures
from neural_netword_for_genetic import NeuralNetWork
from read_all import play


class ThreadExecutor:
    def __init__(self, max_parallel_tasks=1000):
        self.max_parallel_tasks = max_parallel_tasks
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel_tasks)
        self.now_working = 0
        self.futures = []
        self.history = []

    def reset(self):
        self.futures = []
        self.history = []

    def is_max_job(self):
        return self.now_working >= self.max_parallel_tasks

    def do_job(self, pieces, mw, mb, ow, ob):
        future = self.executor.submit(self.main_job, pieces, mw, mb, ow, ob)
        self.futures.append(future)

    def main_job(self, pieces, mw, mb, ow, ob):
        self.now_working += 1
        nn = NeuralNetWork(mw, mb, ow, ob)
        score = play(pieces, nn)
        self.now_working -= 1
        self.history.append([score, [mw, mb, ow, ob]])
