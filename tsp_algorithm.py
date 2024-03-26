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


class Individual:
    def __init__(self, *args, **kwargs):
        self.state = []
        if "state" in kwargs.keys():
            for ele in kwargs["state"]:
                self.state.append(ele)
        if "parent1" in kwargs.keys():
            for ele in kwargs["parent1"]:
                self.state.append(ele)
            # self.state = kwargs["parent1"]
        if "parent2" in kwargs.keys():
            for ele in kwargs["parent2"]:
                self.state.append(ele)
        if "parent3" in kwargs.keys():
            for ele in kwargs["parent3"]:
                self.state.append(ele)

    def __str__(self):
        return str(self.state)

    def add(self, numb : int):
        self.state.append(numb)

    def check(self):
        check_arr = [0 for it in range(0, len(self.state))]
        for x in self.state:
            if check_arr[x] == 1:
                return False
            check_arr[x] = 1
        return True

    def fix(self):
        check_arr = [0 for it in range(0, len(self.state))]
        for x in self.state:
            check_arr[x] += 1
        unfill = []
        for it in range(0, len(self.state)):
            if check_arr[it] == 0:
                unfill.append(it)

        if len(unfill) > 0:
            random.shuffle(unfill)
            for index in range(0, len(self.state)):
                if check_arr[self.state[index]] > 1 and len(unfill) > 0:
                    check_arr[self.state[index]] -= 1
                    self.state[index] = unfill[0]
                    unfill.pop(0)

        if not self.check():
            raise Exception(f"Wrong {len(unfill)}, {self.state}")

    def mutate(self, fit_func):#fix this mutate
        index = random.randint(0, len(self.state) - 1)
        index1 = random.randint(0, max(0, index - 1))
        index2 = random.randint(min(index + 1, len(self.state) - 1), len(self.state) - 1)
        new_child = self.state
        if index1 >= 0 and self.state[index1] != self.state[index]:
            new_child = swap_ele(self.state, index1, index)
        if index2 <= len(self.state) - 1 and self.state[index2] != self.state[index]:
            new_child1 = swap_ele(self.state, index2, index)
            if fit_func(new_child) > fit_func(new_child1):
                self.state = new_child1
            else:
                self.state = new_child



class TSP:
    MAX = 200
    INF = 10000000000

    def __init__(self, **kwargs):
        self.dis = create_distance_lst(kwargs["n"], kwargs["points"])

    def get_min(self, population, fit):
        ans = TSP.INF
        for state in population:
            ans = min(ans, fit(state.state))
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
            index1 = random.randint(0, size_random)
            index2 = random.randint(0, size_random)
            if population[index1].state != population[index2].state:
                return population[index1], population[index2]

    def reproduce(self, parent1, parent2):
        index = random.randint(1, len(parent1.state) - 1)
        arr = [
            Individual(parent1=parent1.state[0: index], parent2=parent2.state[index:]),
            Individual(parent1=parent2.state[0: index], parent2=parent1.state[index:]),
            Individual(parent1=parent1.state[index:], parent2=parent2.state[0:index]),
            Individual(parent1=parent2.state[index:], parent2=parent1.state[0:index])
        ]
        index1 = index
        while index1 == index:
            index1 = random.randint(1, len(parent1.state) - 1)
            if index1 < index:
                index, index1 = index1, index
        a1 = [parent1.state[0:index], parent2.state[index: index1], parent2.state[index1:]]
        a2 = [parent2.state[0:index], parent1.state[index:index1], parent1.state[index1:]]

        for x in range(0, 3):
            # print(a1, a2, index, index1)
            random.shuffle(a1)
            random.shuffle(a2)
            arr.append(Individual(parent1=a1[0], parent2=a1[1], parent3=a1[2]))
            arr.append(Individual(parent1=a2[0], parent2=a2[1], parent3=a2[2]))
        # for x in arr:
        #     print(x.state)
        for x in arr:
            x.fix()
            x.check()
        return arr

    def get_sorted_by_weigth(self, population, fit_func):
        population.sort(key=lambda x: fit_func(x.state))
        return population

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
                # print(child_lst)
                for child in child_lst:
                    child.mutate(fit_func) #fix mutate
                    new_population.append(child)
                if len(new_population) > 10000:
                    break
            new_population = unique(new_population)
            delt = max(-500, self.get_min(population, fit_func) - self.get_min(new_population, fit_func))

            if delt > 0:
                population = new_population
            else:
                print(delt, t)
                if math.exp(-delt / t) > 0.0000001:
                    population = new_population
                else:
                    break
            if len(population) == 1:
                break
            loop_count += 1
        result_state = self.get_sorted_by_weigth(population, fit_func)[0]
        result = fit_func(result_state.state)
        return result_state.state, result


class BruteForce(TSP):
    def __init__(self, *args, **kwargs):
        super().__init__(n=kwargs["n"], points=kwargs["points"])

    def solve(self, population, fit_func):
        if len(population) <= 1:
            return 0
        return self.get_min(population, fit_func)






