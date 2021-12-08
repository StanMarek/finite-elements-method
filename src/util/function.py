import math

import numpy as np
from util.const import (THREE_POINT_KEYS, THREE_POINT_VALUES, TWO_POINT_KEYS,
                        TWO_POINT_VALUES)


def print_matrix(matrix):
    np.set_printoptions(precision=5)
    print(np.matrix(matrix))


def fun_x(x):
    return 5 * x ** 2 + 3 * x + 6


def fun_xy(x, y):
    return 5 * x ** 2 * y ** 2 + 3 * x * y + 6


def gauss_1dim(points):
    if points == 2:
        outcome = TWO_POINT_VALUES[0] * fun_x(
            TWO_POINT_KEYS[0]) + TWO_POINT_VALUES[1] * fun_x(TWO_POINT_KEYS[1])
        return outcome

    elif points == 3:
        outcome = THREE_POINT_VALUES[0] * fun_x(THREE_POINT_KEYS[0]) + THREE_POINT_VALUES[1] * fun_x(
            THREE_POINT_KEYS[1]) + THREE_POINT_VALUES[2] * fun_x(THREE_POINT_KEYS[2])
        return outcome

    else:
        print('Wrong points input')
        return -math.inf


def gauss_2dim(points):
    if points == 2:  # 4
        outcome = 0
        for y in range(points):
            for x in range(points):
                outcome += TWO_POINT_VALUES[x] * TWO_POINT_VALUES[y] * \
                    fun_xy(THREE_POINT_KEYS[x], THREE_POINT_KEYS[y])
        return outcome

    elif points == 3:  # 9
        outcome = 0
        for y in range(points):
            for x in range(points):
                outcome += THREE_POINT_VALUES[x] * THREE_POINT_VALUES[y] * fun_xy(THREE_POINT_KEYS[x],
                                                                                  THREE_POINT_VALUES[y])
        return outcome

    else:
        print('Wrong points input')
        return -math.inf


def dN_dKsi(eta):
    return [
        (-0.25 * (1 - eta)),
        (0.25 * (1 - eta)),
        (0.25 * (1 + eta)),
        (-0.25 * (1 + eta))
    ]


def dN_dEta(ksi):
    return [
        (-0.25 * (1 - ksi)),
        (-0.25 * (1 + ksi)),
        (0.25 * (1 + ksi)),
        (0.25 * (1 - ksi))
    ]


def shape_function(ksi, eta):
    return [
        (0.25 * (1 - ksi) * (1 - eta)),
        (0.25 * (1 + ksi) * (1 - eta)),
        (0.25 * (1 + ksi) * (1 + eta)),
        (0.25 * (1 - ksi) * (1 + eta)),
    ]


def pithagorean_distance(x_1, x_2, y_1, y_2):
    x_diff = x_2 - x_1
    y_diff = y_2 - y_1
    return math.sqrt(
        pow(x_diff, 2) + pow(y_diff, 2)
    )


def multiply_vector_scalar(vector, scalar):
    multiplied = [float] * len(vector)
    for i in range(len(vector)):
        multiplied[i] = vector[i] * scalar

    return multiplied

    
def multiply_vector_vectort(vector):
    size = len(vector)
    multiplied = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            multiplied[i][j] += vector[i] * vector[j]

    # print("mulitplied vector")
    # print_matrix(multiplied)

    return multiplied


def agregation(grid):
    h = np.zeros((grid.nN, grid.nN))
    p = np.zeros(grid.nN)

    for element_number in range(grid.nE):
        element = grid.elements[element_number]
        id = element.ID
        for i in range(4):
            for j in range(4):
                h[id[i]-1][id[j]-1] += element.H[i][j] + element.H_bc[i][j]

            p[id[i]-1] += element.P[i]

    return h, p
