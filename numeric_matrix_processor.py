import math
import sys
from typing import List, Optional


def read_matrix() -> Optional[List[List]]:
    dim_a = [int(val) for val in input("Enter matrix size: ").split(" ")]
    print("Enter matrix: ")
    a = []
    for r in range(0, dim_a[0]):
        row = [int(val) if val.isdigit() else float(val) for val in input().split(" ")]
        if len(row) != dim_a[1]:
            return None
        a.append(row)
    return a


def add_matrices():
    a = read_matrix()
    if a is None:
        print("ERROR")
        return
    b = read_matrix()
    if b is None:
        print("ERROR")
        return
    if (len(a), len(a[0])) != (len(b), len(b[0])):
        print("ERROR")
        return
    c = [[el_a + el_b for el_a, el_b in zip(sublist1, sublist2)] for sublist1, sublist2 in zip(a, b)]
    for row_c in c:
        print(*row_c)


def matrix_scalar_multiplication():
    a = read_matrix()
    if a is None:
        print("ERROR")
        return
    constant = input()
    constant = int(constant) if constant.isdigit() else float(constant)
    c = [[constant * el for el in row] for row in a]
    for row_c in c:
        print(*row_c)


def _transpose_matrix(a: List, row_length: int, col_length: int) -> List:
    temp = []
    for i in range(0, col_length):
        for j in range(0, row_length):
            temp.append(a[i + j * col_length])
    return temp


def maindiag_transpose(a: List[List]) -> List[List]:
    row_length = len(a)
    col_length = len(a[0])
    a = [el for row in a for el in row]
    temp = _transpose_matrix(a, row_length, col_length)
    j = 0
    b = []
    while j < row_length * col_length:
        b.append(temp[j:j + row_length])
        j += row_length
    return b


def horizontal_transpose(a: List[List]) -> List[List]:
    row_length = len(a)
    temp = [[el for el in row] for row in a]
    for r in range(0, row_length // 2):
        temp[r], temp[row_length - r - 1] = temp[row_length - r - 1], temp[r]
    return temp


def sidediag_transpose(a: List[list]) -> List[List]:
    a = horizontal_transpose(a)
    a = maindiag_transpose(a)
    return horizontal_transpose(a)


def vertical_transpose(a: List[List]) -> List[List]:
    a = maindiag_transpose(a)
    a = horizontal_transpose(a)
    return maindiag_transpose(a)


def transpose_matrix():
    print_transpose_menu()
    choice = int(input("Your choice: "))
    a = read_matrix()
    if a is None:
        print("ERROR")
        return
    recipe = transpose_menu_map.get(choice)
    if recipe is not None:
        print_matrix(recipe(a))


def multiply_matrices():
    a = read_matrix()
    if a is None:
        print("ERROR")
        return
    b = read_matrix()
    if b is None:
        print("ERROR")
        return
    if len(a[0]) != len(b):
        print("ERROR")
        return
    n_ar = len(a)
    n_ac = len(a[0])
    n_br = len(b)
    n_bc = len(b[0])
    a = [el for row in a for el in row]
    b = _transpose_matrix([el for row in b for el in row], n_br, n_bc)
    # print(a)
    # print(b)
    temp = []
    i = 0
    while i < n_ar * n_ac:
        j = 0
        while j < n_br * n_bc:
            temp.append(sum([el_a * el_b for (el_a, el_b) in zip(a[i:i + n_ac], b[j:j + n_br])]))
            j += n_br
        i += n_ac
    # print(temp)
    j = 0
    c = []
    while j < n_ar * n_bc:
        c.append(temp[j:j + n_bc])
        j += n_bc
    print_matrix(c)


def _compute_minor(a: List[List], i: int, j: int) -> List[List]:
    b = []
    for row in range(0, len(a)):
        temp = []
        for col in range(0, len(a[0])):
            if row != i and col != j:
                temp.append(a[row][col])
        if len(temp) > 0:
            b.append(temp)
    return b


def _compute_determinant_recursive(a: List[List], i: int, j: int) -> float:
    b = _compute_minor(a, i, j)
    if len(b) == 2:
        return math.pow(-1, i + j) * (b[0][0] * b[1][1] - b[0][1] * b[1][0])
    _det = 0
    for k in range(0, len(b[0])):
        _det += b[0][k] * _compute_determinant_recursive(b, 0, k)
    return math.pow(-1, i + j) * _det


def _compute_determinant(a: List[List]) -> float:
    if len(a) == 1:
        return a[0][0]
    if len(a) == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    _det = 0
    for i in range(0, len(a)):
        _det += a[0][i] * _compute_determinant_recursive(a, 0, i)
    return _det


def compute_determinant():
    a = read_matrix()
    if a is None:
        print("ERROR")
        return
    print(f"The result is:\n{_compute_determinant(a)}")


def _compute_inverse(a: List[List]) -> List[List]:
    _inverse = [[0 for _ in row] for row in a]
    n = len(a)
    for i in range(0, n):
        for j in range(0, n):
            _inverse[i][j] = _compute_determinant_recursive(a, i, j)
    return _inverse


def compute_inverse():
    a = read_matrix()
    if a is None:
        print("ERROR")
        return
    _det = _compute_determinant(a)
    if _det == 0.0:
        print("This matrix doesn't have an inverse.")
        return
    _inverse = [[(1/_det) * el for el in row] for row in maindiag_transpose(_compute_inverse(a))]
    print_matrix(_inverse)


def print_matrix(a: List[List]):
    for row in a:
        print(*row)


def terminate_program():
    sys.exit()


def print_menu():
    print("1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("4. Transpose matrix")
    print("5. Calculate a determinant")
    print("6. Inverse matrix")
    print("0. Exit")


def print_transpose_menu():
    print("1. Main diagonal")
    print("2. Side diagonal")
    print("3. Vertical line")
    print("4. Horizontal line")


def main():
    while True:
        print_menu()
        choice = int(input("Your choice: "))
        recipe = menu_map.get(choice)
        if recipe is not None:
            recipe()


if __name__ == "__main__":
    menu_map = {
        1: add_matrices,
        2: matrix_scalar_multiplication,
        3: multiply_matrices,
        4: transpose_matrix,
        5: compute_determinant,
        6: compute_inverse,
        0: terminate_program,
    }
    transpose_menu_map = {
        1: maindiag_transpose,
        2: sidediag_transpose,
        3: vertical_transpose,
        4: horizontal_transpose,
    }
    main()