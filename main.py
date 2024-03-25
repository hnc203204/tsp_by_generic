import math
import random
import create_test

from file_ope import *
from func import *
from tsp_algorithm import *



parent = []
MAX = 4000000
dis = []
INF = 10000000000


def generate_permutation(index: int, n : int, mask : int, state):
    if index == n:
        parent.append(state)
        return
    if len(parent) > MAX:
        return
    for it in range(0, n):
        if (mask & (1 << it)) == 0:
            generate_permutation(index + 1, n, mask | (1 << it), state + str(it))

def solve(**kwargs):
    n = 0
    points = []
    if "direction" in kwargs.keys():
        n, points = read_file(kwargs["direction"])
    else:
        n, points = read_console()
    global dis, parent
    parent = []
    generate_permutation(0, n, 0, "")

    dis = create_distance_lst(n, points)
    def fit(state):
        total = 0
        for index in range(0, len(state) - 1):
            total += dis[int(state[index])][int(state[index + 1])]
        return total
    try:
        algo = GA(n = n, points = points)
    except:
        raise Exception("Error at GA")

    try:
        algo1 = BruteForce(n = n, points= points)
    except:
        raise Exception("Error at BF")
    print(algo.solve(population=parent[0: min(len(parent), 10000)], fit_func=fit), algo1.solve(parent, fit_func=fit))
    return algo.solve(population=parent[0: min(len(parent), 100)], fit_func=fit)[1] == algo1.solve(parent, fit_func=fit)
    # return 0


if __name__ == "__main__":
    lst = [
        1, 1, 1, 5, 5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10
    ]
    # create_test.create_test(number_of_test=len(lst), lst = lst)
    cnt = 0
    for x in range(0, len(lst)):
        cnt += solve(direction=f"test/test{x}.txt")

    print(cnt)