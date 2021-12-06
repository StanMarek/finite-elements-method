import numpy as np
from model.element import check_element_boundary_condition
from model.grid import Grid
from model.universal_element import UniversalElement, UniversalElementSide
from util.function import print_matrix
from util.h_matrix import (calculate_h_for_element, calculate_h_for_ip)
from util.integral import dN_dX, dN_dY
from util.jacobian import jacobian


def main() -> None:
    #grid = Grid(0.2, 0.1, 5, 4)
    grid = Grid(0.1, 0.1, 4, 4)
    #grid = Grid(0.25, 0.25, 2, 2)
    grid.display()

    el = UniversalElement(2)
    # el.display()

    k_t = 25
    alpha = 300
    t_amb = 1200

    for element_number in range(grid.nE):
        set_of_hi_matrix = []
        for integration_point in range(el.nPoints):
            j, det_j = jacobian(element_number, integration_point, el, grid)
            hi_matrix = calculate_h_for_ip(
                dN_dX(el, j),
                dN_dY(el, j),
                det_j,
                k_t,
                integration_point
            )
            set_of_hi_matrix.append(hi_matrix)

        h_matrix = calculate_h_for_element(set_of_hi_matrix)
        grid.elements[element_number].set_H(h_matrix)

        det_j_side, side_choice = check_element_boundary_condition(
            grid, element_number)

        print("Element {}".format(element_number + 1))
        for j in range(4):
            if side_choice[j] == 1:
                print(1)
            else:
                print(0)

        h_bc = calculate_hbc_for_element(det_j_side, side_choice, el, alpha)
        p = calculate_p_for_element(det_j, side_choice, el, alpha, t_amb)
        grid.elements[element_number].set_Hbc(h_bc)
        grid.elements[element_number].set_P(p)

    for i in range(grid.nE):
        print('Element {} matrix H'.format(i + 1))
        print_matrix(grid.elements[i].H)
        print('Element {} matrix Hbc'.format(i + 1))
        print_matrix(grid.elements[i].H_bc)

    global_h_matrix, global_p_vector = agregation(grid)
    print_matrix(global_h_matrix)
    print(global_p_vector)

    np.savetxt("hmatrix.csv", global_h_matrix, delimiter=";")


def calculate_hbc_for_element(det_j, sides_with_bc, universal_element: UniversalElement, alpha):
    sides_matrix_array = []
    sum = np.zeros((4, 4))
    for i in range(4):
        if sides_with_bc[i] == 1:
            side_number = i
            side_hbc = calculate_hbc_for_side(
                det_j[side_number], side_number, universal_element, alpha)
            sides_matrix_array.append(side_hbc)

    print("ilosc bokow z warunkiem brzegowym: {}".format(len(sides_matrix_array)))
    if len(sides_matrix_array) > 0:
        print("Jest macierz hbc")
        for i in range(4):
            for j in range(4):
                for k in range(len(sides_matrix_array)):
                    sum[i][j] += sides_matrix_array[k][i][j]

    return sum


def calculate_hbc_for_side(det_j, side_number: int, element: UniversalElement, alpha):
    hbc_side = np.zeros((4, 4))
    hbc_point_1 = calculate_hbc_for_ip(
        element.sides[side_number].points[0].N, element.sides[side_number].points[0].weight)
    hbc_point_2 = calculate_hbc_for_ip(
        element.sides[side_number].points[1].N, element.sides[side_number].points[1].weight)

    for i in range(4):
        for j in range(4):
            hbc_side[i][j] = (hbc_point_1[i][j] +
                              hbc_point_2[i][j]) * det_j * alpha

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


def agregation(grid: Grid):
    h = np.zeros((grid.nN, grid.nN))
    p = np.zeros(grid.nN)

    for element_number in range(grid.nE):
        element = grid.elements[element_number]
        id = element.ID
        for i in range(4):
            for j in range(4):
                # !!! nie dodawać Hbc teraz !!!
                h[id[i]-1][id[j]-1] += element.H[i][j] + element.H_bc[i][j]

    for element_number in range(grid.nE):
        element = grid.elements[element_number]
        id = element.ID
        for i in range(4):
            p[id[i]-1] += element.P[i]

    return h, p


def calculate_p_for_element(det_j, sides_with_bc, universal_element: UniversalElement, alpha, t_amb):
    set_of_sides_p = []
    p = np.zeros(4)
    for i in range(4):
        if sides_with_bc[i] == 1:
            side_number = i
            vector_p1 = multiply_vector_scalar(
                universal_element.sides[side_number].points[0].N, t_amb)
            vector_p2 = multiply_vector_scalar(
                universal_element.sides[side_number].points[1].N, t_amb)
            print("N", universal_element.sides[side_number].points[1].N)
            print("vector p2", vector_p2)
            p_side_vector = multiply_vector_scalar(
                vector_p1, universal_element.sides[side_number].points[0].weight) + multiply_vector_scalar(
                vector_p2, universal_element.sides[side_number].points[1].weight
            )

            set_of_sides_p.append(p_side_vector)

    if len(set_of_sides_p) > 0:
        for i in range(4):
            for k in range(len(set_of_sides_p)):
                p[i] += alpha * set_of_sides_p[k][i] * det_j
    print("wektor p", p)
    return p


def multiply_vector_scalar(vector, scalar):
    multiplied = []
    for i in range(len(vector)):
        multiplied.append(vector[i] * scalar)

    return multiplied


if __name__ == '__main__':
    main()
