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
    
  def print(self):
    print('Matrix dN/dKsi\n', np.matrix(self.matrix_dNdKsi))
    print('Matrix dN/dEta\n', np.matrix(self.matrix_dNdEta))



def jacobian(e42d: Element4_2D, grid: Grid):
  dXdKsi = [0.0] * e42d.nPoints
  dYdEta = [0.0] * e42d.nPoints
  J = [[[0 for x in range(2)] for y in range(2)] for z in range(e42d.nPoints)]
  for i in range(e42d.nPoints):
    for j in range(4):
      dXdKsi[i] += X[j] * e42d.matrix_dNdKsi[i][j] 
      dYdEta[i] += Y[j] * e42d.matrix_dNdEta[i][j]
      J[i][0][0] = dXdKsi[i]
      J[i][1][1] = dYdEta[i]

  print("dXdKsi", np.matrix(dXdKsi))
  print("dYdEta", np.matrix(dYdEta))
  
  for i in range(e42d.nPoints):
    print(f"matrix for point {i + 1}\n", np.matrix(J[i]))
   
  detJ = [0.0] * e42d.nPoints
  inverseDetJ = [0] * e42d.nPoints
  for i in range(len(detJ)):
    detJ[i] = J[i][0][0] * J[i][1][1]
    inverseDetJ[i] = 1/detJ[i]

  print(detJ)
  print(inverseDetJ)

  # for i in range(grid.nE):
  #   for j in range(e42d.nPoints):
  #     print(1)

