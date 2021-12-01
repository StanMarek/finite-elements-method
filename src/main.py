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
	set_of_hi_matrix = []
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

		det_j_choice, side_choice = check_element_boundary_condition(grid, element_number) 

		for j in range(4):
			if side_choice == 1:
				print(1)


	for i in range(grid.nE):
		print('Element {} matrix H'.format(i + 1))
		print_matrix(grid.elements[i].H)


def check_element_boundary_condition(grid, element_number):
	i = element_number
	det_j = [float] * 4
	side_choice = [int] * 4
	if (grid.nodes[grid.elements[i].ID[0]-1].bc == 1 and 
	grid.nodes[grid.elements[i].ID[1]-1].bc == 1):
		side_choice[element_side_border["B"]] = 1
		det_j[element_side_border["B"]] = pithagorean_distance(
		grid.nodes[grid.elements[i].ID[0]-1].x,
		grid.nodes[grid.elements[i].ID[1]-1].x,
		grid.nodes[grid.elements[i].ID[0]-1].y,
		grid.nodes[grid.elements[i].ID[1]-1].y
	)
	if (grid.nodes[grid.elements[i].ID[1]-1].bc == 1 and
	grid.nodes[grid.elements[i].ID[2]-1].bc == 1):
		side_choice[element_side_border["R"]] = 1
		det_j[element_side_border["R"]] = pithagorean_distance(
		grid.nodes[grid.elements[i].ID[1]-1].x,
		grid.nodes[grid.elements[i].ID[2]-1].x,
		grid.nodes[grid.elements[i].ID[1]-1].y,
		grid.nodes[grid.elements[i].ID[2]-1].y
	)
	if (grid.nodes[grid.elements[i].ID[2]-1].bc == 1 and 
	grid.nodes[grid.elements[i].ID[3]-1].bc == 1):
		side_choice[element_side_border["T"]] = 1
		det_j[element_side_border["T"]] = pithagorean_distance(
		grid.nodes[grid.elements[i].ID[2]-1].x,
		grid.nodes[grid.elements[i].ID[3]-1].x,
		grid.nodes[grid.elements[i].ID[2]-1].y,
		grid.nodes[grid.elements[i].ID[3]-1].y
	)
	if (grid.nodes[grid.elements[i].ID[0]-1].bc == 1 and 
	grid.nodes[grid.elements[i].ID[3]-1].bc == 1):
		side_choice[element_side_border["L"]] = 1
		det_j[element_side_border["L"]] = pithagorean_distance(
		grid.nodes[grid.elements[i].ID[0]-1].x,
		grid.nodes[grid.elements[i].ID[3]-1].x,
		grid.nodes[grid.elements[i].ID[0]-1].y,
		grid.nodes[grid.elements[i].ID[3]-1].y
	)

	return det_j, side_choice


if __name__ == '__main__':
	main()
