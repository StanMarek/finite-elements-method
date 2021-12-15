import numpy as np

from util.const import K_T, RO, C
from util.function import add_matrices, multiply_matrix_scalar, multiply_vector_vectort, print_matrix
from util.integral import dN_dX, dN_dY

def calculate_h_c_for_ip(jac, dV, nOfIp, el):
    
    size = 4
    HdNdX = np.zeros((size, size))
    HdNdY = np.zeros((size, size))
    Hi = np.zeros((size, size))
    Ci = np.zeros((size, size))

    dNdX = dN_dX(el, jac)
    dNdY = dN_dY(el, jac)

    # 1
    HdNdX = multiply_vector_vectort(dNdX[nOfIp])    
    HdNdY = multiply_vector_vectort(dNdY[nOfIp])
    Hi = add_matrices(HdNdX, HdNdY)
    Ci = multiply_vector_vectort(el.points[nOfIp].N)

    Hi = multiply_matrix_scalar(Hi, K_T * dV * el.points[nOfIp].weight)
    Ci = multiply_matrix_scalar(Ci, RO * C * dV * el.points[nOfIp].weight)

    # 2
    # for i in range(size):
    #     for j in range(size):
    #         HdNdX[i][j] = dNdX[nOfIp][i] * dNdX[nOfIp][j]
    #         HdNdY[i][j] = dNdY[nOfIp][i] * dNdY[nOfIp][j]
    #         Ci[i][j] = el.points[nOfIp].N[i] * el.points[nOfIp].N[j]

    #         if el.nPoints == 4:
    #             Hi[i][j] = K_T * (HdNdX[i][j] + HdNdY[i][j]) * dV
    #             Ci[i][j] = C * RO * Ci[i][j] * dV

    #         elif el.nPoints == 9:
    #             Hi[i][j] = K_T * (HdNdX[i][j] + HdNdY[i][j]) * dV * el.points[nOfIp].weight
    #             Ci[i][j] = C * RO * Ci[i][j] * dV * el.points[nOfIp].weight

    return Hi, Ci


def calculate_h_c_for_element(Hi, Ci):

    Hmat = np.zeros((4, 4))
    Cmat = np.zeros((4, 4))

    # 1
    # for i in range(4):
    #     for j in range(4):
    #         for k in range(len(Hi)):
    #             Hmat[i][j] += Hi[k][i][j]
    #             Cmat[i][j] += Ci[k][i][j]

    # 2
    Hmat = add_matrices(*Hi)
    Cmat = add_matrices(*Ci)
    
    return Hmat, Cmat
