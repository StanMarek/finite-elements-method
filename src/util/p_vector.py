import math
from model.universal_element import UniversalElement
import numpy as np
from util.const import ALPHA, T_AMB
from util.function import add_matrices, add_vectors, multiply_vector_scalar


def calculate_p_for_element(det_j, sides_with_bc, universal_element: UniversalElement):

    sides_to_compute = []
    element_p = np.zeros(4)
    
    for side_number in range(4):
        if sides_with_bc[side_number] == 1:
            side = calculate_p_for_side(det_j, side_number, universal_element)
            sides_to_compute.append(side)

    # 1
    # for i in range(4):
    #     for side in sides_to_compute:
    #         element_p[i] += side[i]

    # 2
    if len(sides_to_compute) > 0:
        element_p = add_vectors(*sides_to_compute)

    return element_p


def calculate_p_for_side(det_j, side_number, element: UniversalElement):

    p = np.zeros(4)
    nip = int(math.sqrt(element.nPoints))
    points = []

    # 1
    # if nip == 4:

    #     vector_point1 = calculate_p_for_ip(element.sides[side_number].points[0].N,
    #                                     element.sides[side_number].points[0].weight)
    #     vector_point2 = calculate_p_for_ip(element.sides[side_number].points[1].N,
    #                                     element.sides[side_number].points[1].weight)

    #     for i in range(4):
    #         p[i] = ALPHA * (vector_point1[i] + vector_point2[i]) * det_j[side_number]

    # elif nip == 9:

    #     vector_point1 = calculate_p_for_ip(element.sides[side_number].points[0].N,
    #                                        element.sides[side_number].points[0].weight)
    #     vector_point2 = calculate_p_for_ip(element.sides[side_number].points[1].N,
    #                                        element.sides[side_number].points[1].weight)
    #     vector_point3 = calculate_p_for_ip(element.sides[side_number].points[2].N,
    #                                        element.sides[side_number].points[2].weight)

    #     for i in range(4):
    #         p[i] = ALPHA * (vector_point1[i] + vector_point2[i] + vector_point3[i]
    #                         ) * det_j[side_number]

    # 2
    for ip in range(nip):
        point = calculate_p_for_ip(element.sides[side_number].points[ip].N,
                                    element.sides[side_number].points[ip].weight)
        points.append(point)
    
    if len(points) > 0:
        p = add_vectors(*points)
        p = multiply_vector_scalar(p, ALPHA * det_j[side_number])
  
    return p


def calculate_p_for_ip(N, w):
    
    p = multiply_vector_scalar(N, T_AMB * w)
    
    return p