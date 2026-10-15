import numpy as np
from matrices import matrices


def main():
    number = int(input("Enter the matrix number> "))
    matrix = matrices.get(number)
    if not matrix:
        print(f"Matrix {number} not found")
        return


if __name__ == "__main__":
    main()
