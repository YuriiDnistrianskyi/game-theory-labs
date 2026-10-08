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


def grafical_solution(matrix, t):
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
    
    plt.plot([ls[position]] * 2, [0, v], label="v", linestyle="--")
    
    plt.xlabel("y")
    plt.ylabel("x")
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
