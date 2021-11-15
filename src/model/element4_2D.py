import numpy as np
from util.function import twoPointKeys
from model.grid import Grid

matrix = list[list[any]]

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
    print('Matrix dN/dKsi')
    printMatrix(self.matrix_dNdKsi)
    print('Matrix dN/dEta')
    printMatrix(self.matrix_dNdEta)


def printMatrix(matrix):
  np.set_printoptions(precision=5)
  print(np.matrix(matrix))


def jacobian(nOfElem, nOfIP, e42d: Element4_2D, grid: Grid):
  dXdKsi = dYdEta = dXdEta = dYdKsi = 0.0

  for j in range(4):
    # nodeId = grid.elements[nOfElem].ID[j] - 1
    # dXdKsi += e42d.matrix_dNdKsi[nOfIP][j] * grid.nodes[nodeId].x
    # dYdEta += e42d.matrix_dNdEta[nOfIP][j] * grid.nodes[nodeId].y
    # dXdEta += e42d.matrix_dNdEta[nOfIP][j] * grid.nodes[nodeId].x
    # dYdKsi += e42d.matrix_dNdKsi[nOfIP][j] * grid.nodes[nodeId].y
    dXdKsi += X[j] * e42d.matrix_dNdKsi[nOfIP][j] 
    dYdEta += Y[j] * e42d.matrix_dNdEta[nOfIP][j]

  J = [[0 for y in range(2)] for x in range(2)]
  transposeJ = [[0 for y in range(2)] for x in range(2)]
  J[0][0] = dXdKsi
  J[0][1] = dYdKsi
  J[1][0] = dXdEta
  J[1][1] = dYdEta

  detJ = (J[0][0] * J[1][1]) - (J[0][1] * J[1][0])
  inverseDetJ = 1/detJ

  transposeJ[0][0] = J[1][1]
  transposeJ[0][1] = - J[0][1]
  transposeJ[1][0] = - J[1][0]
  transposeJ[1][1] = J[0][0]
  
  for i in range(2):
    for j in range(2):
      J[i][j] = inverseDetJ * transposeJ[i][j]

  return J

def dNidX(dNdEta: matrix, dNdKsi: matrix, jac: matrix, nOfIP):
  dNidX = [0 for x in range(4)]

  for i in range(4):
    dNidX[i] = jac[0][0] * dNdKsi[nOfIP][i] + jac[0][1] * dNdEta[nOfIP][i]
  return dNidX

def dNidY(dNdEta: matrix, dNdKsi: matrix, jac: matrix, nOfIP):
  dNidY = [0 for x in range(4)]

  for i in range(4):
    dNidY[i] = jac[1][0] * dNdKsi[nOfIP][i] + jac[1][1] * dNdEta[nOfIP][i]

  return dNidY

def dNdX(e42d: Element4_2D, jac: matrix):
  ip = e42d.nPoints
  dNdX = [[] for j in range(ip)]

  for i in range(ip):
    dNdX[i] = dNidX(e42d.matrix_dNdEta, e42d.matrix_dNdKsi, jac, i)

  return dNdX

def dNdY(e42d: Element4_2D, jac: matrix):
  ip = e42d.nPoints
  dNdY = [[] for j in range(ip)]

  for i in range(ip):
    dNdY[i] = dNidY(e42d.matrix_dNdEta, e42d.matrix_dNdKsi, jac, i)

  return dNdY

def calculateHMatrixForIP(dNdX: matrix, dNdY: matrix, dV, k, nOfIp):
  size = len(dNdX)
  HdNdX = [[0 for x in range(size)] for y in range(size)]
  HdNdY = [[0 for x in range(size)] for y in range(size)] 
  Hi = [[0 for x in range(size)] for y in range(size)]

  for i in range(size):
    for j in range(size):
      HdNdX[i][j] = dNdX[nOfIp][i] * dNdX[nOfIp][j] 
      HdNdY[i][j] = dNdY[nOfIp][i] * dNdY[nOfIp][j] 
      Hi[i][j] = k * (HdNdX[i][j] + HdNdY[i][j]) * dV
      
  return Hi

def calculateHMatrixForElem(e42d: Element4_2D, jac: matrix, dV, k):
  H = [[0 for x in range(e42d.nPoints)] for y in range(e42d.nPoints)] 
  _dNdX = dNdX(e42d, jac)
  _dNdY = dNdY(e42d, jac)
  
  for i in range(4):
    for j in range(4):
      for l in range(4):
        H[i][j] += calculateHMatrixForIP(_dNdX, _dNdY, dV, k, l)[i][j]
    
  return H
