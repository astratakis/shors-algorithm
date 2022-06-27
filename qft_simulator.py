from cmath import exp
from numpy import pi
n = 3

def print_qft_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(matrix[i][j], end=" ")
        print()

matrix = [[0 for i in range(1 << n)] for i in range(1 << n)]

for i in range(1 << n):
    matrix[i][0] = 1
    matrix[0][i] = 1

rev = 1 / (1 << n)

def omega(mult: int, rev: float):
    return exp(mult * 2 * pi * 1j * rev)

for i in range(1, 1 << n):
    for j in range(1, 1 << n):
        matrix[j][i] = omega(j, rev)
    rev *= 2

print_qft_matrix(matrix)