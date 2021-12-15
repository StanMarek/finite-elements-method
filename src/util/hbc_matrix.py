import math
import numpy as np
from model.universal_element import UniversalElement

from util.const import ALPHA
from util.function import add_matrices, multiply_matrix_scalar, multiply_vector_vectort


def calculate_hbc_for_element(det_j, sides_with_bc, universal_element: UniversalElement):

    sides_to_compute = []
    element_hbc = np.zeros((4, 4))
    for side_number in range(4):
        if sides_with_bc[side_number] == 1:
            side = calculate_hbc_for_side(
                det_j, side_number, universal_element)
            sides_to_compute.append(side)

    # 1
    # for i in range(4):
    #     for j in range(4):
    #         for side in sides_to_compute:
    #             element_hbc[i][j] += side[i][j]

    # 2
    if len(sides_to_compute) > 0:
        element_hbc = add_matrices(*sides_to_compute)

    return element_hbc


def calculate_hbc_for_side(det_j, side_number, element: UniversalElement):

    npc = int(math.sqrt(element.nPoints))
    side_hbc = np.zeros((4, 4))

    # 1
    # if npc == 2:

    #     hbc_point1 = calculate_hbc_for_ip(element.sides[side_number].points[0].N,
    #                                     element.sides[side_number].points[0].weight)
    #     hbc_point2 = calculate_hbc_for_ip(element.sides[side_number].points[1].N,
    #                                   element.sides[side_number].points[1].weight)

    #     for i in range(4):
    #         for j in range(4):
    #             side_hbc[i][j] = ALPHA * (hbc_point1[i][j] + hbc_point2[i]
    #                             [j]) * det_j[side_number]

    # elif npc == 3:
       
    #     hbc_point1 = calculate_hbc_for_ip(element.sides[side_number].points[0].N,
    #                                       element.sides[side_number].points[0].weight)
    #     hbc_point2 = calculate_hbc_for_ip(element.sides[side_number].points[1].N,
    #                                       element.sides[side_number].points[1].weight)
    #     hbc_point3 = calculate_hbc_for_ip(element.sides[side_number].points[2].N,
    #                                       element.sides[side_number].points[2].weight)

    #     for i in range(4):
    #         for j in range(4):
    #             side_hbc[i][j] = ALPHA * (hbc_point1[i][j] + hbc_point2[i][j] + hbc_point3[i][j]) * det_j[side_number]

    # 2
    points_hbc = []

    for i in range(npc):
        hbc_for_point = calculate_hbc_for_ip(element.sides[side_number].points[i].N,
                                             element.sides[side_number].points[i].weight)
        points_hbc.append(hbc_for_point)

    side_hbc = add_matrices(*points_hbc)
    side_hbc = multiply_matrix_scalar(side_hbc, ALPHA * det_j[side_number])

    return side_hbc


def calculate_hbc_for_ip(N, w):

    point_hbc = multiply_vector_vectort(N)

    # 1
    # for i in range(4):
    #     for j in range(4):
    #         point_hbc[i][j] = w * point_hbc[i][j]

    # 2
    point_hbc = multiply_matrix_scalar(point_hbc, w)

    return point_hbc
