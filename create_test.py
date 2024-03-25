
import random
import file_ope

def create_test(number_of_test, lst):
    for __ in range(0, number_of_test):
        n = lst[__]
        points = []
        check = {}
        for ___ in range(0, n):
            while True:
                x = random.randint(0, 1000)
                y = random.randint(0, 1000)
                if not (x, y) in check.keys():
                    check[(x, y)] = 1
                    points.append((x, y))
                    break
        print(n, points)
        file_ope.write_file(n, points, __)


