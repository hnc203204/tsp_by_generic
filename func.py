

def euclid_dis(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def schedule(loops_count):
    return 100 - loops_count + 0.00000001

def create_distance_lst(n, points):
    dis = [[0 for i in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            if i == j:
                dis[i][j] = 0
            else:
                dis[i][j] = euclid_dis(points[i], points[j])
    return dis

def swap_string(string, index1, index2):
    char_list = list(string)
    char_list[index1], char_list[index2] = char_list[index1], char_list[index2]
    new_string = "".join(char_list)
    return new_string

