import matplotlib.pyplot as plt
import numpy as np
from matrices import matrices


def main():
    number = int(input("Enter the matrix number> "))
    matrix = matrices.get(number)
    if not matrix:
        print(f"Matrix {number} not found")
        return

    if len(matrix) == 2:
        t = "2xN"
    elif len(matrix[0]) == 2:
        t = "Mx2"
    else:
        print("Incorrect size of matrix")
        return

    grafical_solution(np.array(matrix), t)

def search_saddle_point(m: list[list[int]]):
    l = len(m)
    c = len(m[0])

    maxmin = max([min(l) for l in m])
    minmax = min([max(m[:, c]) for c in range(c)])

    print(f"Maxmin: {maxmin}")
    print(f"Minmax: {minmax}")

    if maxmin == minmax:
        points = []
        for i in range(l):
            for j in range(c):
                if m[i, j] == maxmin and m[i, j] == min(m[i]) and m[i, j] == max(m[:, j]):
                    points.append(m[i, j])
        if len(points) > 1:
            print(f"Several({len(points)}) saddle points are found: {points[0]}")
        elif len(points) == 1:
            print(f"One saddle point is found: {points[0]}")
    else:
        print("Not saddle point")

def grafical_solution(matrix, t):
    search_saddle_point(matrix)

    funcs = []
    ls = np.linspace(0, 1, 100)

    n = len(matrix[0]) if t == "2xN" else len(matrix)
         
    for i in range(n):
        func = matrix[1, i] + (matrix[0, i] - matrix[1, i]) * ls if t == "2xN" else matrix[i, 0] + (matrix[i, 1] - matrix[i, 0]) * ls
        funcs.append(func)

        l = f"A{i + 1}A`{i + 1}" if t == "2xN" else f"B{i + 1}B`{i + 1}"
        plt.plot(ls, func, label=l)
    
    funcs = np.array(funcs)
    func = np.min(funcs, axis=0) if t == "2xN" else np.max(funcs, axis=0)
    position = np.argmax(func) if t == "2xN" else np.argmin(func)
        
    v = func[position]
    
    print(f"v = {v}")

    plt.scatter(ls[position], v)
    plt.plot([ls[position]] * 2, [0, v], label="v", linestyle="--")
    
    plt.xlabel("y")
    plt.ylabel("x")
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
