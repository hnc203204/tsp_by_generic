import math
import random

parent = []
MAX = 1000000
dis = []
INF = 10000000000


def read_file(direction):
    points = []
    with open(direction, "r") as file:
        n = int(file.readline())
        for iter in range(0, n):
            x, y = map(int, file.readline().split(" "))
            print(x, y)
            points.append((x, y))
    return n, points

def read_console():
    n = int(input())
    points = []
    for it in range(0, n):
        x, y = map(int, input().split(" "))
        points.append((x, y))
    return n, points

def get_sorted_by_weigth(population, fit_func):
    population.sort(key=lambda x : fit_func(x))
    return population


def swap_string(string, index1, index2):
    char_list = list(string)
    char_list[index1], char_list[index2] = char_list[index1], char_list[index2]
    new_string = "".join(char_list)
    return new_string

def mutate(child):
    index = random.randint(0, len(child) - 1)
    for it in range(0, len(child)):
        try:
            if it != int(child[index]):
                a = 0
                b = 0
                current = 0
                try:
                    if index - 1 >= 0:
                        a = dis[int(child[index - 1])][it]
                        current = dis[int(child[index - 1])][int(child[index])]

                except:
                    raise IndexError("1")


                try:
                    if index + 1 < len(child):
                        b = dis[it][int(child[index + 1])]
                        current += dis[int(child[index])][int(child[index + 1])]
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
def random_choice(population):
    size_random = int(math.sqrt(len(population)))
    while True:
        index1 = random.randint(0, size_random)
        index2 = random.randint(0, size_random)
        if population[index1] != population[index2]:
            return population[index1], population[index2]


def check(child):
    check_arr = [0 for it in range(0, len(child))]
    for x in child:
        if check_arr[int(x)] == 1:
            return False
        check_arr[int(x)] = 1
    return True


def fix(child):
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
                new_child = child[0 : index] + str(unfill[0])
                if index + 1 < len(child):
                    child = new_child + child[index + 1:]
                unfill.pop(0)
                check_arr[int(child[index])] -= 1
    return child

def reproduce(parent1, parent2):
    index = random.randint(1, len(parent1) - 1)
    arr = [
        parent1[0: index] + parent2[index:],
        parent2[0: index] + parent1[index:]
    ]
    rd_index = random.randint(0, 1)
    return fix(arr[rd_index])


def get_min(population, fit):
    ans = INF
    for state in population:
        ans = min(ans, fit(state))
    return ans

def schedule(loops_count):
    return 100 - loops_count + 0.00000001

def generic_algorithm(population, fit_func):
    loop_count = 0
    while True:
        new_population = []
        t = schedule(loop_count)
        if t < 0.0000000000001:
            break
        sorted_population = get_sorted_by_weigth(population, fit_func)
        for i in range(0, len(population)):
            parent1, parent2 = random_choice(sorted_population)
            child = reproduce(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        delt = get_min(population, fit_func) - get_min(new_population, fit_func)
        if delt > 0:
            population = new_population
        else:
            print(delt, t)
            if math.exp(-delt + 0.000001) - math.exp(t) > 0.2:
                population = new_population
            else:
                break
        loop_count += 1
    return get_sorted_by_weigth(population, fit_func)[0]




def generate_permutation(index: int, n : int, mask : int, state):
    if index == n:
        parent.append(state)
        return
    if len(parent) > MAX:
        return
    for it in range(0, n):
        if (mask & (1 << it)) == 0:
            generate_permutation(index + 1, n, mask | (1 << it), state + str(it))

def euclid_dis(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def create_distance_lst(n, points):
    dis = [[0 for i in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            if i == j:
                dis[i][j] = 0
            else:
                dis[i][j] = euclid_dis(points[i], points[j])
    return dis

def solve(**kwargs):
    n = 0
    points = []
    if "direction" in kwargs.keys():
        n, points = read_file(kwargs["direction"])
    else:
        n, points = read_console()
    generate_permutation(0, n, 0, "")
    print(parent)
    global dis
    dis = create_distance_lst(n, points)
    def fit(state):
        total = 0
        for index in range(0, len(state) - 1):
            total += dis[int(state[index])][int(state[index + 1])]
        return total
    print(generic_algorithm(parent, fit))




if __name__ == "__main__":
    solve(direction="test.txt")