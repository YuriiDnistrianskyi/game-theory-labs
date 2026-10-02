import matplotlib.pyplot as plt
import numpy as np
from matrices import matrices


def main():
    number = int(input("Enter the matrix number> "))
    matrix = matrices.get(number)
    if not matrix:
        print(f"Matrix {number} not found")
        return
    steps = int(input("Enter the number of steps> "))
    brown_robinson_method(np.array(matrix), steps)


def calculate_frequency(p, n, current):
    new_p = []
    for i in range(len(p)):
        if i == current:
            new = ((n * p[i]) + 1) / (n + 1)
        else:
            new = (n * p[i]) / (n + 1)
        new_p.append(new)
    return np.array(new_p)


def get_a_strategy(matrix, q):
    maxs = [sum(matrix[i] * q) for i in range(len(matrix))]
    strategy = np.argmax(maxs)
    return strategy, max(maxs)


def get_b_strategy(matrix, p):
    mins = [sum(matrix[:, j] * p) for j in range(len(matrix[0]))]
    strategy = np.argmin(mins)
    return strategy, min(mins)


def brown_robinson_method(matrix, steps):
    m = len(matrix)
    n = len(matrix[0])

    i = 0
    j = 0

    p = np.array([1] + [0] * (m - 1))
    q = np.array([1] + [0] * (n - 1))

    vs = []


    for s in range(2, steps + 1):
        i, a = get_a_strategy(matrix, q)
        j, b = get_b_strategy(matrix, p)

        p = calculate_frequency(p, s, i)
        q = calculate_frequency(q, s, j)

        v = (a + b) / 2
        vs.append(v)

    plt.plot(range(2, steps + 1), vs)
    plt.xlabel("Steps")
    plt.ylabel("Value of the game")
    plt.title("Brown-Robinson Method")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
