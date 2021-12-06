import math

import numpy as np

TWO_POINT_KEYS = [(-1 / math.sqrt(3)), (1 / math.sqrt(3))]
THREE_POINT_KEYS = [(-math.sqrt(3 / 5)), 0, (math.sqrt(3 / 5))]

TWO_POINT_VALUES = [1, 1]
THREE_POINT_VALUES = [(5 / 9), (8 / 9), (5 / 9)]


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
