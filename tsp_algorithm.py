from abc import abstractmethod
import math
import random
from func import *
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
        size_random = int(math.sqrt(len(population)))
        while True:
            try:
                index1 = random.randint(0, size_random)
                index2 = random.randint(0, size_random)
                if population[index1] != population[index2]:
                    return population[index1], population[index2]
            except:
                raise Exception(f"Exception at {index1}, {index2}")

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
                    new_child = child[0: index] + str(unfill[0])
                    if index + 1 < len(child):
                        child = new_child + child[index + 1:]
                    unfill.pop(0)
                    check_arr[int(child[index])] -= 1
        return child

    def reproduce(self, parent1, parent2):
        index = random.randint(1, len(parent1) - 1)
        arr = [
            parent1[0: index] + parent2[index:],
            parent2[0: index] + parent1[index:]
        ]
        rd_index = random.randint(0, 1)
        return self.fix(arr[rd_index])

    def get_sorted_by_weigth(self, population, fit_func):
        population.sort(key=lambda x: fit_func(x))
        return population

    def mutate(self, child):
        index = random.randint(0, len(child) - 1)
        for it in range(0, len(child)):
            try:
                if it != int(child[index]):
                    a = 0
                    b = 0
                    current = 0
                    try:
                        if index - 1 >= 0:
                            a = self.dis[int(child[index - 1])][it]
                            current = self.dis[int(child[index - 1])][int(child[index])]

                    except:
                        raise IndexError("1")

                    try:
                        if index + 1 < len(child):
                            b = self.dis[it][int(child[index + 1])]
                            current += self.dis[int(child[index])][int(child[index + 1])]
                    except:
                        raise IndexError("2")

                    if a + b < current:
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
            if t < 0.0000000000001:
                break
            sorted_population = self.get_sorted_by_weigth(population, fit_func)
            for i in range(0, len(population)):
                parent1, parent2 = self.random_choice(sorted_population)
                child = self.reproduce(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            print(population)
            print(new_population)
            delt = self.get_min(population, fit_func) - self.get_min(new_population, fit_func)
            if delt > 0:
                population = new_population
            else:
                print(delt, t)
                if math.exp(-delt + 0.000001) - math.exp(t) > 0.00001:
                    population = new_population
                else:
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






