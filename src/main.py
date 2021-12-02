import numpy as np
from model.element import check_element_boundary_condition
from model.grid import Grid
from model.universal_element import UniversalElement, UniversalElementSide
from util.function import print_matrix
from util.h_matrix import (calculate_h_matrix_for_element,
                           calculate_h_matrix_for_ip)
from util.integral import dN_dX, dN_dY
from util.jacobian import jacobian


def main() -> None:
    grid = Grid(0.2, 0.1, 5, 4)
    # grid.display()

    el = UniversalElement(2)
    # el.display()

    k_t = 30

    for element_number in range(grid.nE):
        set_of_hi_matrix = []
        for integration_point in range(el.nPoints):
            j, det_j = jacobian(element_number, integration_point, el, grid)
            hi_matrix = calculate_h_matrix_for_ip(
                dN_dX(el, j),
                dN_dY(el, j),
                det_j,
                k_t,
                integration_point
            )
            set_of_hi_matrix.append(hi_matrix)

        h_matrix = calculate_h_matrix_for_element(set_of_hi_matrix)
        grid.elements[element_number].set_H(h_matrix)

        det_j_side, side_choice = check_element_boundary_condition(
            grid, element_number)

        print("Element {}".format(element_number + 1))
        for j in range(4):
            if side_choice[j] == 1:
                print(1)
            else:
                print(0)

        h_bc = calculate_hbc_for_element(det_j_side, side_choice, el)
        grid.elements[element_number].set_Hbc(h_bc)

    for i in range(grid.nE):
        print('Element {} matrix H'.format(i + 1))
        print_matrix(grid.elements[i].H)
        print('Element {} matrix Hbc'.format(i + 1))
        print_matrix(grid.elements[i].H_bc)


def calculate_hbc_for_element(det_j, sides_with_bc, universal_element: UniversalElement):
    sides_matrix_array = []
    sum = np.zeros((4, 4))
    for i in range(4):
        if sides_with_bc[i] == 1:
            side_number = i
            side_hbc = calculate_hbc_for_side(
                det_j[side_number], side_number, universal_element)
            sides_matrix_array.append(side_hbc)

    print("ilosc bokow z warunkiem brzegowym: {}".format(len(sides_matrix_array)))
    if len(sides_matrix_array) > 0:
        print("Jest macierz hbc")
        for i in range(4):
            for j in range(4):
                for k in range(len(sides_matrix_array)):
                    sum[i][j] += sides_matrix_array[k][i][j]

    return sum


def calculate_hbc_for_side(det_j, side_number: int, element: UniversalElement):
    hbc_side = np.zeros((4, 4))
    hbc_point_1 = calculate_hbc_for_ip(
        element.sides[side_number].points[0].N, element.sides[side_number].points[0].weight)
    hbc_point_2 = calculate_hbc_for_ip(
        element.sides[side_number].points[0].N, element.sides[side_number].points[0].weight)

    for i in range(4):
        for j in range(4):
            hbc_side[i][j] = (hbc_point_1[i][j] + hbc_point_2[i][j]) * det_j

    print("Hbc dla sciany")
    print_matrix(hbc_side)
    return hbc_side


def calculate_hbc_for_ip(N, w):
    hc = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            hc[i][j] = w * (N[i] * N[j])
    print("Hc dla punktu")
    print_matrix(hc)

    return hc


if __name__ == '__main__':
    main()
