from model.element import Element
from model.universal_element import *
from model.grid import Grid
from model.node import Node
from util.function import gauss_1dim, gauss_2dim
from util.h_matrix import calculate_h_matrix_for_element, calculate_h_matrix_for_ip
from util.integral import dN_dX, dN_dY
from util.jacobian import jacobian


def main() -> None:
    grid = Grid(0.2, 0.1, 5, 4)
    grid.display()

    el = UniversalElement(2)
    el.display()

    k_t = 30
    set_of_hi_matrix = [] * 4
    for element_number in range(grid.nE):
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

    for i in range(grid.nE):
        print('Element {} matrix H'.format(i + 1))
        print_matrix(grid.elements[i].H)

if __name__ == '__main__':
    main()
