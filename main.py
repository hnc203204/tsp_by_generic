
parent = []
MAX = 1000000
dis = []


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

def get_weight(population, fit_func):
    weight = []
    for state in population:
        weight.append(fit_func(state))
    return weight

def mutate(parent1, parent2):



def generic_algorithm(population, fit_func):
    while True:
        new_population = []
        weight = get_weight(population, fit_func)


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
    if "directions" in kwargs.keys():
        n, points = read_file(kwargs["direction"])
    else:
        n, points = read_console()
    generate_permutation(0, n, 0, "")
    dis = create_distance_lst(n, points)
    def fit(state):
        total = 0
        for index in range(0, len(state) - 1):
            total += dis[int(state[index])][int(state[index + 1])]
        return total
    generate_permutation(parent, fit)




if __name__ == "__main__":
    solve(direction="test.txt")