import numpy as np
from util.integral import matrix


def calculate_h_for_ip(dNdX: matrix, dNdY: matrix, dV, k, nOfIp):
    size = len(dNdX)
    HdNdX = np.zeros((size, size))
    HdNdY = np.zeros((size, size))
    Hi = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            HdNdX[i][j] = dNdX[nOfIp][i] * dNdX[nOfIp][j]
            HdNdY[i][j] = dNdY[nOfIp][i] * dNdY[nOfIp][j]
            Hi[i][j] = k * (HdNdX[i][j] + HdNdY[i][j]) * dV

    return Hi

# def calculateHMatrixForElem(e42d: Element4_2D, J, dV, kT):
#   H = [[0 for x in range(4)] for y in range(4)]

#   for i in range(4):
#     for j in range(4):
#       for k in range(4):
#         _dNdX = dNdX(e42d, J)
#         _dNdY = dNdY(e42d, J)
#         H[i][j] += calculateHMatrixForIP(_dNdX, _dNdY, dV, kT, k)[i][j]

#   return H


def calculate_h_for_element(Hi):
    H = np.zeros((4, 4))

    for i in range(4):
        for j in range(4):
            for k in range(4):
                H[i][j] += Hi[k][i][j]

    return H
