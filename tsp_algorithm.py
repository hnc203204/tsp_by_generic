from abc import abstractmethod
import math
import random
from func import *


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list


class TSP:
    MAX = 200
    INF = 10000000000

    def __init__(self, **kwargs):
        self.dis = create_distance_lst(kwargs["n"], kwargs["points"])

    def get_min(self, population, fit):
        ans = TSP.INF
        for state in population:
            ans = min(ans, fit(state))
        return ans

    @abstractmethod
    def solve(self, population, fit_func):
        pass

class GA(TSP):

    def __init__(self, *args, **kwargs):
        super().__init__(n=kwargs["n"], points = kwargs["points"])

    def random_choice(self, population):
        size_random = int(len(population) / 2)
        while True:
            index1 = random.randint(0, size_random)
            index2 = random.randint(0, size_random)
            if population[index1] != population[index2]:
                return population[index1], population[index2]

    def check(self, child):
        check_arr = [0 for it in range(0, len(child))]
        for x in child:
            if check_arr[int(x)] == 1:
                return False
            check_arr[int(x)] = 1
        return True

    def fix(self, child):
        check_arr = [0 for it in range(0, len(child))]
        for x in child:
            check_arr[int(x)] += 1
        unfill = []
        for it in range(0, len(child)):
            if check_arr[it] == 0:
                unfill.append(it)

        if len(unfill) > 0:
            random.shuffle(unfill)
            for index in range(0, len(child)):
                if check_arr[int(child[index])] > 1 and len(unfill) > 0:
                    check_arr[int(child[index])] -= 1
                    new_child = child[0: index] + str(unfill[0])
                    if index + 1 < len(child):
                        child = new_child + child[index + 1:]
                    unfill.pop(0)

        if not self.check(child):
            raise Exception(f"Wrong {len(unfill)}, {child}")
        return child

    def reproduce(self, parent1, parent2):
        index = random.randint(1, len(parent1) - 1)
        arr = [
            self.fix(parent1[0: index] + parent2[index:]),
            self.fix(parent2[0: index] + parent1[index:]),
            self.fix(parent1[index:] + parent2[0:index]),
            self.fix(parent2[index:] + parent1[0:index])
        ]
        index1 = random.randint(1, len(parent1) - 1)
        if index1 < index:
            index, index1 = index1, index
        a1 = [parent1[0:index], parent2[index: index1], parent2[index1:]]
        a2 = [parent2[0:index], parent1[index:index1], parent1[index1:]]
        for x in range(0, 3):
            random.shuffle(a1)
            random.shuffle(a2)
            arr.append(self.fix(a1[0] + a1[1] + a1[2]))
            arr.append(self.fix(a2[0] + a2[1] + a2[2]))

        return arr

    def get_sorted_by_weigth(self, population, fit_func):
        population.sort(key=lambda x: fit_func(x))
        return population

    def mutate(self, child):#fix this mutate
        index = random.randint(0, len(child) - 1)
        for it in range(0, len(child)):
            try:
                if it != int(child[index]):
                    for it1 in range(0, len(child)):
                        if child[it1] == str(it):
                            child = swap_string(child, it1, index)
                            break
            except:
                raise Exception(f"Exception at: {child}")
        return child

    def solve(self, population, fit_func):
        loop_count = 0
        if len(population) <= 1:
            return population[0], 0
        while True:
            new_population = []
            t = schedule(loop_count)
            if t < 0.000001:
                break
            sorted_population = self.get_sorted_by_weigth(population, fit_func)
            for i in range(0, len(population)):
                parent1, parent2 = self.random_choice(sorted_population) #fix random choice
                child_lst = self.reproduce(parent1, parent2)
                for child in child_lst:
                    child = self.mutate(child) #fix mutate
                    new_population.append(child)
                if len(new_population) > 10000:
                    break
            new_population = unique(new_population)
            delt = max(-500, self.get_min(population, fit_func) - self.get_min(new_population, fit_func))

            if delt > 0:
                population = new_population
            else:
                # print(delt, t)
                if math.exp(-delt / t) > 0.0000001:
                    population = new_population
                else:
                    break
            if len(population) == 1:
                break
            loop_count += 1
        result_state = self.get_sorted_by_weigth(population, fit_func)[0]
        result = fit_func(result_state)
        return result_state, result


class BruteForce(TSP):
    def __init__(self, *args, **kwargs):
        super().__init__(n=kwargs["n"], points=kwargs["points"])

    def solve(self, population, fit_func):
        if len(population) <= 1:
            return 0
        return self.get_min(population, fit_func)






