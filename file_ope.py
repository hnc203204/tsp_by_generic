def read_file(direction):
    points = []
    with open(direction, "r") as file:
        n = int(file.readline())
        for iter in range(0, n):
            x, y = map(int, file.readline().split(" "))
            points.append((x, y))
    return n, points

def read_console():
    n = int(input())
    points = []
    for it in range(0, n):
        x, y = map(int, input().split(" "))
        points.append((x, y))
    return n, points

def write_file(n, points, count):
    with open(f"test/test{count}.txt", "x") as file:
        file.write(str(n))
        for x in points:
            file.write(f"\n{x[0]} {x[1]}")