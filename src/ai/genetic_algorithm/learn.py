from read_all import play, get_pieces
import numpy as np
from neural_netword_for_genetic import NeuralNetWork
from time import time
from multi_thread_play import ThreadExecutor
import pickle
from copy import deepcopy
import concurrent.futures

mutation_rate = 0.1


def select_random_with_bias(lst):
    weights = (np.arange(len(lst))[::-1]) ** 4  # 先頭にある方がより大きな重みを持つように指数関数を適用
    selected_indices = np.random.choice(len(lst), size=2, replace=False, p=weights / np.sum(weights))
    return [lst[i] for i in selected_indices]


def make_random_arrays(input_num, middle_num):
    mw = np.random.rand(input_num, middle_num) - 0.5
    mb = np.random.rand(middle_num) - 0.5
    ow = np.random.rand(middle_num, 1) - 0.5
    ob = np.random.rand() - 0.5
    return [mw, mb, ow, ob]


def mating(array1: np.array, array2: np.array):
    """
    遺伝的アルゴリズムの交配
    :param array1: 交配する配列の1つ目
    :param array2: 交配する配列の2つ目
    :return: 交配された2つの配列
    """
    # ランダムなブールマスクを生成
    bool_mask = np.random.choice([True, False], size=array1.shape)

    # 交配された配列を生成
    child1 = array1.copy()
    child2 = array2.copy()
    child1[bool_mask] = array2[bool_mask]
    child2[bool_mask] = array1[bool_mask]

    mutation_mask = np.random.rand(*array1.shape) < mutation_rate
    child1[mutation_mask] = (np.random.rand(*array1.shape) - 0.5)[mutation_mask]
    child2[mutation_mask] = (np.random.rand(*array1.shape) - 0.5)[mutation_mask]

    return child1, child2


def mate_of_float(a, b):
    return1 = b if np.random.randn() < 0.5 else a
    return2 = a if np.random.randn() < 0.5 else b
    if np.random.randn() < mutation_rate:
        return1 = np.random.randn() - 0.5
    if np.random.randn() < mutation_rate:
        return2 = np.random.randn() - 0.5
    return return1, return2


population_per_generation = 1000

start = time()
# population_list = [make_random_arrays(17, 10) for _ in range(population_per_generation)]
population_list = pickle.load(open(r"C:\Users\aiueo\tetris_ai\src\ai\genetic_algorithm\test2.pickle", "rb"))

# pieces = get_pieces()
# executor = ThreadExecutor()
for _ in range(100):
    score_list = []
    pieces = get_pieces()
    # executor.reset()
    # for i in population_list:
    #     executor.do_job(pieces, *i)
    # concurrent.futures.wait(executor.futures)
    # print(len(executor.history))
    # exit()
    for idx, i in enumerate(population_list):
        nn = NeuralNetWork(*i)
        score = play(pieces, nn)
        score_list.append(score)
        if idx % 40 == 0:
            print(idx)
    sorted_genes = [gene for _, gene in sorted(zip(score_list, population_list), key=lambda x: x[0], reverse=True)]
    population_list = sorted_genes[:50]
    origin_population_list = deepcopy(population_list)
    print(np.unique(score_list, return_counts=True))
    while len(population_list) < population_per_generation:
        arr1, arr2 = select_random_with_bias(origin_population_list)
        new_ = []
        for i, j in zip(arr1, arr2):
            if type(i) == float:
                c1, c2 = mate_of_float(i, j)
            else:
                c1, c2 = mating(i, j)
            new_.append((c1, c2))
        population_list.append([n[0] for n in new_])
        population_list.append([n[1] for n in new_])
    with open("test2.pickle", "wb") as f:
        pickle.dump(population_list, f)
