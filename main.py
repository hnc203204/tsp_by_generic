import math
import random
import create_test

from file_ope import *
from func import *
from tsp_algorithm import *
import copy


MAX = 50000
dis = []
INF = 10000000000

class Generate:

    def __init__(self):
        self.parent = []
    def generate_permutation(self, index: int, n : int, mask : int, state : Individual):
        if index == n:
            self.parent.append(state)
            return
        if len(self.parent) > MAX:
            return
        for it in range(0, n):
            if (mask & (1 << it)) == 0:
                new_state = copy.deepcopy(state)
                new_state.add(it)
                # print(new_state, state)
                self.generate_permutation(index + 1, n, mask | (1 << it), new_state)

def solve(**kwargs):
    n = 0
    points = []
    if "direction" in kwargs.keys():
        n, points = read_file(kwargs["direction"])
    else:
        n, points = read_console()
    global dis, parent
    parent = []
    gener_per = Generate()
    print(n)
    gener_per.generate_permutation(0, n, 0, Individual())

    dis = create_distance_lst(n, points)
    # for state in gener_per.parent:
    #     print(state)
    def fit(state):
        total = 0
        try:
            for index in range(0, len(state) - 1):
                total += dis[state[index]][state[index + 1]]
        except:
            raise Exception(f"Loi o {index} {state}")
        return total
    try:
        algo = GA(n = n, points = points)
    except:
        raise Exception("Error at GA")
    #
    # try:
    #     algo1 = BruteForce(n = n, points= points)
    # except:
    #     raise Exception("Error at BF")
    print(algo.solve(population=gener_per.parent, fit_func=fit))


if __name__ == "__main__":
    lst = [
        10, 10, 10, 20, 20, 20, 30, 30, 30, 100, 100, 100
    ]
    # create_test.create_test(number_of_test=len(lst), lst = lst)
    # cnt = 0
    for x in range(3, len(lst)):
        solve(direction=f"test/test{x}.txt")

    # print(cnt)