from model.universal_element import UniversalElement
import numpy as np
from util.const import ALPHA, T_AMB

from util.function import multiply_vector_scalar

def calculate_p_for_element(det_j, sides_with_bc, universal_element: UniversalElement):
    sides_to_compute = []
    element_p = np.zeros(4)
    
    for side_number in range(4):
        if sides_with_bc[side_number] == 1:
            side = calculate_p_for_side(det_j, side_number, universal_element)
            sides_to_compute.append(side)

    for i in range(4):
        for side in sides_to_compute:
            element_p[i] += side[i]

    #print("P element", element_p)
    return element_p


def calculate_p_for_side(det_j, side_number, element: UniversalElement):
    p = np.zeros(4)
    vector_point1 = calculate_p_for_ip(element.sides[side_number].points[0].N,
                                       element.sides[side_number].points[0].weight)
    vector_point2 = calculate_p_for_ip(element.sides[side_number].points[1].N,
                                       element.sides[side_number].points[1].weight)

    for i in range(4):
        p[i] = ALPHA * (vector_point1[i] + vector_point2[i]) * det_j[side_number]

    #print("P vector side", p)    
    return p


def calculate_p_for_ip(N, w):
    vector = multiply_vector_scalar(N, w)
    p = multiply_vector_scalar(vector, T_AMB)
    #print("P vector point", p)
    return p