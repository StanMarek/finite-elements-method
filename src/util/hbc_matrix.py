import numpy as np
from model.universal_element import UniversalElement

from util.const import ALPHA
from util.function import multiply_vector_vectort


def calculate_hbc_for_element(det_j, sides_with_bc, universal_element: UniversalElement):

    sides_to_compute = []
    element_hbc = np.zeros((4, 4))
    for side_number in range(4):
        if sides_with_bc[side_number] == 1:
            side = calculate_hbc_for_side(
                det_j, side_number, universal_element)
            sides_to_compute.append(side)

    #print("Sides with bc {}".format(len(sides_to_compute)))
    for i in range(4):
        for j in range(4):
            for side in sides_to_compute:
                element_hbc[i][j] += side[i][j]

    # print("element hbc")
    # print_matrix(element_hbc)

    return element_hbc


def calculate_hbc_for_side(det_j, side_number: int, element: UniversalElement):

    npc = element.nPoints
    side_hbc = np.zeros((4, 4))

    if npc == 4:

        hbc_point1 = calculate_hbc_for_ip(element.sides[side_number].points[0].N,
                                        element.sides[side_number].points[0].weight)
        hbc_point2 = calculate_hbc_for_ip(element.sides[side_number].points[1].N,
                                      element.sides[side_number].points[1].weight)

        for i in range(4):
            for j in range(4):
                side_hbc[i][j] = ALPHA * (hbc_point1[i][j] + hbc_point2[i]
                                [j]) * det_j[side_number]

    elif npc == 9:
       
        hbc_point1 = calculate_hbc_for_ip(element.sides[side_number].points[0].N,
                                          element.sides[side_number].points[0].weight)
        hbc_point2 = calculate_hbc_for_ip(element.sides[side_number].points[1].N,
                                          element.sides[side_number].points[1].weight)
        hbc_point3 = calculate_hbc_for_ip(element.sides[side_number].points[2].N,
                                          element.sides[side_number].points[2].weight)

        for i in range(4):
            for j in range(4):
                side_hbc[i][j] = ALPHA * (hbc_point1[i][j] + hbc_point2[i][j] + hbc_point3[i][j]) * det_j[side_number]


    return side_hbc


def calculate_hbc_for_ip(N, w):

    point_hbc = multiply_vector_vectort(N)

    for i in range(4):
        for j in range(4):
            point_hbc[i][j] = w * point_hbc[i][j]

    return point_hbc
