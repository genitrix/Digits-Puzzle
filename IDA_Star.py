# Using IDA* Algorithm
from itertools import chain

MAX_TIMES = 100

# 计算逆序数，判断有无解
def inverseNum(source):
    cnt = 0
    pos0 = 0
    seq = list(chain(*source))
    i_ = 0
    while i_ < 16:
        if seq[i_] == 0:
            pos0 = i_
        j_ = i_ + 1
        while j_ < 16:
            if seq[i_] > seq[j_]:
                cnt = cnt + 1
            j_ = j_ + 1
        i_ = i_ + 1
    cnt += abs(pos0 / 4 - 3) + abs(pos0 % 4 - 3)
    if cnt % 2 == 1:
        return 1
    else:
        return 0


# 计算曼哈顿距离
def manhattan(node, destination):
    cost = 0
    for i in range(4):
        for j in range(4):
            num = node[i][j]
            x, y = destination[num]
            cost += abs(x - i) + abs(y - j)

    return cost


def successors(node, destination):
    x, y = 0, 0
    for i in range(4):
        for j in range(4):
            if node[i][j] == 0:
                x, y = i, j
    success = []
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for i, j in moves:
        a_, b_ = x + i, y + j
        if -1 < a_ < 4 and -1 < b_ < 4:
            temp = [[num for num in col] for col in node]
            temp[x][y] = temp[a_][b_]
            temp[a_][b_] = 0
            success.append(temp)

    return sorted(success, key=lambda x: manhattan(x, destination))


def is_goal(node):
    index = 1
    for line in node:
        for col in line:
            if index != col:
                break
            index += 1
    return index == 16


def search(route, g, boundary, destination):
    node = route[-1]
    f = g + manhattan(node, destination)
    if f > boundary:
        return f
    if is_goal(node):
        return -1
    minimum = 9999
    for success in successors(node, destination):
        if success not in route:
            route.append(success)
            t = search(route, g + 1, boundary, destination)
            if t == -1:
                return -1
            if t < minimum:
                minimum = t
            route.pop()

    return minimum


def ida_star(source):
    # 目标状态
    destination = {}
    number = 1
    for a in range(4):
        for b in range(4):
            destination[number] = (a, b)
            number += 1
        destination[0] = (3, 3)
    boundary = manhattan(source, destination)
    route = [source]

    while True:
        t = search(route, 0, boundary, destination)
        if t == -1:
            return route, boundary
        if t > MAX_TIMES:
            return [], boundary
        boundary = t


class Source():
    source = {1: [[1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 11, 12], [13, 10, 14, 15]],
              2: [[5, 1, 3, 4], [2, 7, 8, 12], [9, 6, 11, 15], [0, 13, 10, 14]],
              3: [[0, 1, 3, 4], [5, 2, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]],
              4: [[1, 2, 3, 4], [5, 0, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]],
              5: [[1, 2, 3, 4], [0, 5, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]],
              6: [[5, 1, 3, 4], [0, 11, 6, 7], [2, 9, 10, 8], [13, 14, 12, 15]],
              7: [[2, 0, 3, 4], [1, 5, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]],
              8: [[1, 6, 2, 4], [5, 12, 11, 3], [0, 9, 8, 7], [13, 10, 14, 15]],
              9: [[0, 1, 3, 4], [5, 11, 6, 7], [2, 9, 10, 8], [13, 14, 12, 15]]}
    des = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


if __name__ == "__main__":

    src = Source.source[9]
    (path, bound) = ida_star(src)
    step = 0
    for p in path:
        print('step', step)
        step += 1
        for row in p:
            print(row)
