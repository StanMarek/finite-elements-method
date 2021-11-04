import numpy as np
from util.function import twoPointKeys
from model.grid import Grid

def dNdKsi(eta):
  return [(-0.25*(1-eta)), (0.25*(1-eta)), (0.25*(1+eta)), (-0.25*(1+eta))]

def dNdEta(ksi):
  return [(-0.25*(1-ksi)), (-0.25*(1+ksi)), (0.25*(1+ksi)), (0.25*(1-ksi))]

eta = [twoPointKeys[0], twoPointKeys[0], twoPointKeys[1], twoPointKeys[1]]
ksi = [twoPointKeys[0], twoPointKeys[1], twoPointKeys[1], twoPointKeys[0]]
X = [0, 0.025, 0.025, 0]
Y = [0, 0, 0.025, 0.025]

class Element4_2D:
  def __init__(self, nPoints: int):  
    ndN = 4
    self.nPoints = nPoints
    self.matrix_dNdKsi = [[0 for x in range(ndN)] for y in range(nPoints)] 
    self.matrix_dNdEta = [[0 for x in range(ndN)] for y in range(nPoints)]

    for i in range(nPoints):
      for j in range(ndN):
        self.matrix_dNdKsi[i][j] = dNdKsi(eta[i])[j]
        self.matrix_dNdEta[i][j] = dNdEta(ksi[i])[j]
    
  def display(self):
    print('Matrix dN/dKsi\n', np.matrix(self.matrix_dNdKsi))
    print('Matrix dN/dEta\n', np.matrix(self.matrix_dNdEta))


def printMatrix(matrix):
  print(np.matrix(matrix))


def jacobian(nOfElem, nOfIP, e42d: Element4_2D, grid: Grid):
  dXdKsi = dYdEta = dXdEta = dYdKsi = 0.0

  for j in range(4):
    # dXdKsi += e42d.matrix_dNdKsi[nOfIP][j] * grid.nodes[grid.elements[nOfElem].ID[j] -1].x
    # dYdEta += e42d.matrix_dNdEta[nOfIP][j] * grid.nodes[grid.elements[nOfElem].ID[j] -1].y
    # dXdEta += e42d.matrix_dNdEta[nOfIP][j] * grid.nodes[grid.elements[nOfElem].ID[j] -1].x
    # dYdKsi += e42d.matrix_dNdEta[nOfIP][j] * grid.nodes[grid.elements[nOfElem].ID[j] -1].y
    dXdKsi += X[j] * e42d.matrix_dNdKsi[nOfIP][j] 
    dYdEta += Y[j] * e42d.matrix_dNdEta[nOfIP][j]

  J = transposeJ = [[0 for y in range(2)] for x in range(2)]
  J[0][0] = dXdKsi;
  J[0][1] = dYdKsi;
  J[1][0] = dXdEta;
  J[1][1] = dYdEta;

  detJ = (J[0][0] * J[1][1]) - (J[0][1] * J[1][0])
  inverseDetJ = 1/detJ

  transposeJ[0][0] = J[1][1]
  transposeJ[0][1] = - J[0][1]
  transposeJ[1][0] = - J[1][0]
  transposeJ[1][1] = J[0][0]
  
  for i in range(2):
    for j in range(2):
      J[i][j] = inverseDetJ * transposeJ[i][j]

  printMatrix(J)
  return J