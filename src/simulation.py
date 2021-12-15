import os
from model.grid import Grid
from model.universal_element import UniversalElement
from util.const import TIME_START, TIME_STEP, TIME_STOP
import numpy as np
from termcolor import colored
from util.function import add_matrices, add_vectors, agregation, multiply_matrix_scalar, solve_system

from util.h_c_matrix import calculate_h_c_for_element, calculate_h_c_for_ip
from util.hbc_matrix import calculate_hbc_for_element
from util.integral import dN_dX, dN_dY
from util.jacobian import jacobian
from util.p_vector import calculate_p_for_element


def simulation(grid: Grid, element: UniversalElement):

  for time in range(TIME_START, TIME_STOP + TIME_STEP, TIME_STEP):

    for element_number in range(grid.nE):

        # matrix H for element
        set_of_hi_matrix = []
        set_of_ci_matrix = []

        for integration_point in range(element.nPoints):

            j, det_j = jacobian(
              element_number, 
              integration_point, 
              element, 
              grid)

            hi_matrix, ci_matrix = calculate_h_c_for_ip(
              j,
              det_j,
              integration_point,
              element)

            set_of_hi_matrix.append(hi_matrix)
            set_of_ci_matrix.append(ci_matrix)

        h_matrix, c_matrix = calculate_h_c_for_element(
          set_of_hi_matrix, set_of_ci_matrix)

        grid.elements[element_number].set_H(h_matrix)
        grid.elements[element_number].set_C(c_matrix)

        # matrix Hbc and vector P for element
        det_j_sides, side_choice = grid.elements[element_number].check_element_boundary_condition(grid)
        h_bc = calculate_hbc_for_element(det_j_sides, side_choice, element)
        p = calculate_p_for_element(det_j_sides, side_choice, element)
        grid.elements[element_number].set_Hbc(h_bc)
        grid.elements[element_number].set_P(p)

    h_global, p_global, c_global = agregation(grid)
    temp = solve_system(h_global, p_global)

    for node in range(grid.nN):
      temp[node] = grid.nodes[node].t

    c_dt = multiply_matrix_scalar(c_global, 1/TIME_STEP)
    c_dt_t0 = np.matmul(c_dt, temp)

    h_global = add_matrices(h_global, c_dt)
    p_global = add_vectors(p_global, c_dt_t0)
    temp = solve_system(h_global, p_global)

    for i in range(grid.nN):
      grid.nodes[i].t = temp[i]

    # save_to_file("Hg", h_global, time)
    # save_to_file("Cg", c_global, time)
    # save_to_file("Pg", p_global, time)
    # save_to_file("Temp", temp, time)

    print(colored("time:", "green"), time, colored("\tmin:", "blue"),
            "{:.3f}".format(min(temp)), colored("\tmax:", "red"), "{:.3f}".format(max(temp)))


def save_to_file(filename, object, iteration):

  OUTPUT_DIR = "simulation_output"

  if not(os.path.exists(OUTPUT_DIR)): 
    os.mkdir(OUTPUT_DIR)

  path = "{}/{}_{}.csv".format(OUTPUT_DIR, filename, iteration)
  np.savetxt(path, object, delimiter=";")