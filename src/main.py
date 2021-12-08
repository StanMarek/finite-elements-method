import numpy as np

from model.element import check_element_boundary_condition
from model.grid import Grid
from model.universal_element import UniversalElement
from util.const import ALPHA, T_AMB
from util.function import agregation, multiply_vector_scalar, print_matrix
from util.h_matrix import calculate_h_for_element, calculate_h_for_ip
from util.hbc_matrix import calculate_hbc_for_element
from util.integral import dN_dX, dN_dY
from util.jacobian import jacobian


def main() -> None:
    #grid = Grid(0.2, 0.1, 5, 4)
    #grid = Grid(0.1, 0.1, 4, 4)
    grid = Grid(0.025, 0.025, 2, 2)
    #grid = Grid(1, 1, 2, 2)
    #grid = Grid(2, 2, 2, 2)
    #grid.display()

    el = UniversalElement(2)
    # el.display()

    for element_number in range(grid.nE):
        # matrix H for element
        set_of_hi_matrix = []
        for integration_point in range(el.nPoints):
            j, det_j = jacobian(element_number, integration_point, el, grid)
            hi_matrix = calculate_h_for_ip(
                dN_dX(el, j),
                dN_dY(el, j),
                det_j,
                integration_point
            )
            set_of_hi_matrix.append(hi_matrix)

        h_matrix = calculate_h_for_element(set_of_hi_matrix)
        grid.elements[element_number].set_H(h_matrix)

        # matrix Hbc and vector P for element
        det_j_sides, side_choice = check_element_boundary_condition(
            grid, element_number)
        
        # print("Element {}".format(element_number + 1))
        # for j in range(4):
        #     if side_choice[j] == 1:
        #         print(1)
        #     else:
        #         print(0)

        h_bc = calculate_hbc_for_element(det_j_sides, side_choice, el)
        p = calculate_p_for_element(det_j_sides, side_choice, el)
        grid.elements[element_number].set_Hbc(h_bc)
        grid.elements[element_number].set_P(p)

    # for i in range(grid.nE):
    #     print('Element {} matrix H'.format(i + 1))
    #     print_matrix(grid.elements[i].H)
    #     print('Element {} matrix Hbc'.format(i + 1))
    #     print_matrix(grid.elements[i].H_bc)

    global_h_matrix, global_p_vector = agregation(grid)
    temp = np.linalg.solve(global_h_matrix, global_p_vector)

    print("Global H:")
    print_matrix(global_h_matrix)
    print("Global P:", global_p_vector)
    print("Temp: ", temp)

    #np.savetxt("hmatrix.csv", global_h_matrix, delimiter=";")



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


if __name__ == '__main__':
    main()
