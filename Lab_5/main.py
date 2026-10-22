import numpy as np
from matrices import matrices
from scipy.optimize import linprog


def main():
    number = int(input("Enter the matrix number> "))
    matrix = matrices.get(number)
    if not matrix:
        print(f"Matrix {number} not found")
        return

    line_solve(np.array(matrix))

def positive_matrix(m: list[list[int]]):
    min_valus = min([min(l) for l in m])
    if min_valus <= 0:
        m = m + abs(min_valus) + 1
        return m, abs(min_valus) + 1

    return m, 0

def line_solve(m):
    m, n = positive_matrix(m)

    z = linprog(
        c=np.ones(m.shape[0]),
        A_ub=-m.T,
        b_ub=-np.ones(m.shape[1]),
        bounds=(0, None),
        method="highs-ds"
    )

    f = linprog(
        c=-np.ones(m.shape[1]),
        A_ub=m,
        b_ub=np.ones(m.shape[0]),
        bounds=(0, None),
        method="highs-ds"
    )

    if not z.success or not f.success:
            print("Linear programming failed")
            return

    solve_z = sum(z.x)
    solve_f = sum(f.x)

    v = (1 / solve_z) - n
    p = z.x / solve_z
    q = f.x / solve_f

    print(f"v = {v}")
    print(f"p = {p}")
    print(f"q = {q}")

    optimal_strategies_1 = [i + 1 for i, x in enumerate(p) if x != 0]
    optimal_strategies_2 = [i + 1 for i, x in enumerate(q) if x != 0]

    print(f"The optimal strategy for 1 player: {optimal_strategies_1}")
    print(f"The optimal strategy for 2 player: {optimal_strategies_2}")


if __name__ == "__main__":
    main()
