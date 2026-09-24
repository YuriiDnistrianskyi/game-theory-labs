import numpy as np
from matrices import matrices
from node import Node


def main():
    number = int(input("Enter the matrix number> "))
    matrix = matrices.get(number)
    if not matrix:
        print(f"Matrix {number} not found")
        return

    search_saddle_point(np.array(matrix))

def get_criteria(m: list[list[int]]) -> tuple[Node]:
    mins = []
    for i in range(len(m)):
        min_node = Node(m[i][0], [i, 0])
        for j in range(len(m[0])):
            if m[i, j] < min_node:
                min_node = Node(m[i][j], [i, j])
        mins.append(min_node)

    maxs = []
    for j in range(len(m[0])):
        max_node = Node(m[0][j], [0, j])
        for i in range(len(m)):
            if m[i][j] > max_node:
                max_node = Node(m[i][j], [i, j])
        maxs.append(max_node)

    maxmin = (max(mins))
    minmax = (min(maxs))

    return (maxmin, minmax)


def search_saddle_point(m: list[list[int]]):
    l = len(m)
    c = len(m[0])

    maxmin, minmax = get_criteria(m)

    print(f"Maxmin: {maxmin.value}")
    print(f"Minmax: {minmax.value}")

    if maxmin.value == minmax.value:
        points = {}
        for i in range(l):
            for j in range(c):
                if m[i, j] == maxmin.value and m[i, j] == min(m[i]) and m[i, j] == max(m[:, j]):
                    points[(i, j)] = int(m[i, j])

        if len(points.keys()) > 1:
            print(f"Several({len(points.keys())}) saddle points are found")
            for xy, p in points.items():
                print("-" * 20)
                print(f"Some saddle point: {p} - {xy}")
                print(f"The optimal strategy for 1 player: {xy[0]}")
                print(f"The optimal strategy for 2 player: {xy[1]}")
        else:
            xy = next(iter(points))
            p = points[xy] 
            print(f"One saddle point is found: {p} - {xy}")
            print(f"The optimal strategy for 1 player: {xy[0]}")
            print(f"The optimal strategy for 2 player: {xy[1]}")

    else:
        print("Saddle point is not found")
        print(f"The maxmin strategy (for 1 player): {maxmin.xy[0]}")
        print(f"The minmax strategy (for 2 player): {minmax.xy[1]}")
        

if __name__ == "__main__":
    main()