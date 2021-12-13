import numpy as np
from model.universal_element import UniversalElement


def dNi_dX(e42d: UniversalElement, jac, nOfIP):

    dNidX = np.zeros(4)

    for i in range(4):
        dNidX[i] = jac[0][0] * e42d.matrix_dN_dKsi[nOfIP][i] + \
            jac[0][1] * e42d.matrix_dN_dEta[nOfIP][i]

    return dNidX


def dNi_dY(e42d: UniversalElement, jac, nOfIP):

    dNidY = np.zeros(4)

    for i in range(4):
        dNidY[i] = jac[1][0] * e42d.matrix_dN_dKsi[nOfIP][i] + \
            jac[1][1] * e42d.matrix_dN_dEta[nOfIP][i]

    return dNidY


def dN_dX(e42d: UniversalElement, jac):

    ip = e42d.nPoints
    dNdX = [[] for j in range(ip)]

    for i in range(ip):
        dNdX[i] = dNi_dX(e42d, jac, i)

    return dNdX


def dN_dY(e42d: UniversalElement, jac):
    
    ip = e42d.nPoints
    dNdY = [[] for j in range(ip)]

    for i in range(ip):
        dNdY[i] = dNi_dY(e42d, jac, i)

    return dNdY
