import numpy as np
from model.grid import Grid
from model.universal_element import UniversalElement
from util.function import multiply_matrix_scalar


def jacobian(nOfElem, nOfIP, e42d: UniversalElement, grid: Grid):

    dXdKsi = 0.0
    dYdEta = 0.0
    dXdEta = 0.0
    dYdKsi = 0.0

    # test
    # X = [0, 0.25, 0.25, 0]
    # Y = [0, 0, 0.25, 0.25]

    for j in range(4):
        # dev
        nodeId = grid.elements[nOfElem].ID[j] - 1
        dXdKsi += e42d.matrix_dN_dKsi[nOfIP][j] * grid.nodes[nodeId].x
        dYdEta += e42d.matrix_dN_dEta[nOfIP][j] * grid.nodes[nodeId].y
        dXdEta += e42d.matrix_dN_dEta[nOfIP][j] * grid.nodes[nodeId].x
        dYdKsi += e42d.matrix_dN_dKsi[nOfIP][j] * grid.nodes[nodeId].y
        # test
        # dXdKsi += e42d.matrix_dN_dKsi[nOfIP][j] * X[j]
        # dYdEta += e42d.matrix_dN_dEta[nOfIP][j] * Y[j]

    
    J = np.zeros((2, 2))
    inverse_j = np.zeros((2, 2))
    J[0][0] = dXdKsi
    J[0][1] = dYdKsi
    J[1][0] = dXdEta
    J[1][1] = dYdEta

    det_j = (J[0][0] * J[1][1]) - (J[0][1] * J[1][0])
    # det_j = np.linalg.det(J)
    
    inverse_det_j = 1/det_j
    inverse_j[0][0] = J[1][1]
    inverse_j[0][1] = - J[0][1]
    inverse_j[1][0] = - J[1][0]
    inverse_j[1][1] = J[0][0]
    # inverse_j = np.transpose(J)

    1
    for i in range(2):
        for j in range(2):
            J[i][j] = inverse_det_j * inverse_j[i][j]

    #2
    # J = multiply_matrix_scalar(inverse_j, inverse_det_j)
    # J = np.linalg.inv(J)

    return J, det_j
