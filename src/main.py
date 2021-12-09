import numpy as np

from model.element import check_element_boundary_condition
from model.grid import Grid
from model.universal_element import UniversalElement
from util.const import ALPHA, T_AMB, T_INIT, TIME_STEP
from util.function import agregation, multiply_vector_scalar, print_matrix
from util.h_matrix import calculate_h_for_element, calculate_h_for_ip
from util.hbc_matrix import calculate_hbc_for_element
from util.integral import dN_dX, dN_dY
from util.jacobian import jacobian
from util.p_vector import calculate_p_for_element


def main() -> None:
    #grid = Grid(0.2, 0.1, 5, 4)
    grid = Grid(0.1, 0.1, 4, 4)
    #grid = Grid(0.025, 0.025, 2, 2)
    #grid = Grid(1, 1, 2, 2)
    #grid = Grid(2, 2, 2, 2)
    #grid.display()

    el = UniversalElement(2)
    # el.display()

    for element_number in range(grid.nE):
        # matrix H for element
        set_of_hi_matrix = []
        set_of_ci_matrix = []
        for integration_point in range(el.nPoints):
            j, det_j = jacobian(element_number, integration_point, el, grid)
            hi_matrix, ci_matrix = calculate_h_for_ip(
                dN_dX(el, j),
                dN_dY(el, j),
                det_j,
                integration_point,
                el
            )
            set_of_hi_matrix.append(hi_matrix)
            set_of_ci_matrix.append(ci_matrix)
        
        h_matrix, c_matrix = calculate_h_for_element(set_of_hi_matrix, set_of_ci_matrix)
        grid.elements[element_number].set_H(h_matrix)
        grid.elements[element_number].set_C(c_matrix)
        
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

    h_global, p_global, c_global = agregation(grid)
    temp = np.linalg.solve(h_global, p_global)

    print("Global H:")
    print_matrix(h_global)
    print("Global P:", p_global)
    print("Temp: ", temp)
    print("Global C:")
    print_matrix(c_global)
    np.savetxt("hmatrix.csv", h_global, delimiter=";")
    np.savetxt("cmatrix.csv", c_global, delimiter=";")
    np.savetxt("pvector.csv", p_global, delimiter=";")
    np.savetxt("tempvector.csv", temp, delimiter=";")

    t0_vector = []
    for node in range(grid.nN):
        t0_vector.append(grid.nodes[node].t)

    c_dt = multiply_matrix_scalar(c_global, 1/TIME_STEP)
    h_dash = np.add(h_global, c_dt)
    c_dt_t0 = np.matmul(c_dt, t0_vector)
    p_dash = np.add(p_global, c_dt_t0)

    print("H dash:")
    print_matrix(h_dash)
    print("P dash:", p_dash)

    
def multiply_matrix_scalar(matrix, scalar):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j] * scalar

    return matrix


if __name__ == '__main__':
    main()
