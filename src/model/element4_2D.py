import numpy as np
from util.function import twoPointKeys

def dNdKsi(eta):
  return [(-0.25*(1-eta)), (0.25*(1-eta)), (0.25*(1+eta)), (-0.25*(1+eta))]

def dNdEta(ksi):
  return [(-0.25*(1-ksi)), (-0.25*(1+ksi)), (0.25*(1+ksi)), (0.25*(1-ksi))]

eta = [twoPointKeys[0], twoPointKeys[0], twoPointKeys[1], twoPointKeys[1]]
ksi = [twoPointKeys[0], twoPointKeys[1], twoPointKeys[1], twoPointKeys[0]]

class Element4_2D:
  def __init__(self, points):  
    w = points*points
    h = 4

    self.table_dNdKsi = [[0 for x in range(w)] for y in range(h)] 
    self.table_dNdEta = [[0 for x in range(w)] for y in range(h)]
    j = 0
    for i in range(w):
      for j in range(4):
        self.table_dNdKsi[i][j] = dNdKsi(eta[j])[i]
        self.table_dNdEta[i][j] = dNdEta(ksi[j])[i]

  def print(self):
    print(np.matrix(self.table_dNdKsi))
    print(np.matrix(self.table_dNdEta))
    
