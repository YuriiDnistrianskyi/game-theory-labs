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


def calculate_frequency(old_f, n, current):
    new_values = []
    for i in range(len(old_f)):
        if i == current:
            new = ((n * old_f[i]) + 1) / (n + 1)
        else:
            new = (n * old_f[i]) / (n + 1)
        new_values.append(new)
    return np.array(new_values)


def get_a_strategy(matrix, q):
    maxs = [sum(matrix[i] * q) for i in range(len(matrix))]
    strategy = np.argmax(maxs)
    return strategy, max(maxs)


def get_b_strategy(matrix, p):
    mins = [sum(matrix[:, j] * p) for j in range(len(matrix[0]))]
    strategy = np.argmin(mins)
    return strategy, min(mins)


def brown_robinson_method(matrix, steps):
    n =len(matrix)
    m = len(matrix[0])

    i = 0
    j = 0

    p = np.array([1] + [0] * (n - 1))
    q = np.array([1] + [0] * (m - 1))

    vs = [None]

    for s in range(1, steps):
        i, a = get_a_strategy(matrix, q)
        j, b = get_b_strategy(matrix, p)

        p = calculate_frequency(p, s, i)
        q = calculate_frequency(q, s, j)

        v = (a + b) / 2
        vs.append(v)


    plt.plot(range(1, steps + 1), vs)
    plt.xlabel("Steps")
    plt.ylabel("Value of the game")
    plt.title("Brown-Robinson Method")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
