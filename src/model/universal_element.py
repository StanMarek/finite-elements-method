import numpy as np
from util.function import TWO_POINT_KEYS, dN_dEta, dN_dKsi, print_matrix
from model.grid import Grid

eta = [TWO_POINT_KEYS[0], TWO_POINT_KEYS[0], TWO_POINT_KEYS[1], TWO_POINT_KEYS[1]]
ksi = [TWO_POINT_KEYS[0], TWO_POINT_KEYS[1], TWO_POINT_KEYS[1], TWO_POINT_KEYS[0]]
X = [0, 0.025, 0.025, 0]
Y = [0, 0, 0.025, 0.025]

class Point:
  def __init__(self, x, y, v):
    self.ksi = x
    self.eta = y
    self.value = v
    self.N = [] * 4

class UniversalElementSide: 
  def __init__(self, n_points):
    self.number_of_ip = n_points
    self.points = [Point] * self.number_of_ip
      
class UniversalElement:
  def __init__(self, number_of_points: int):
    nd_n = 4
    self.nPoints = number_of_points ** 2
    self.matrix_dNd_Ksi = [[0 for x in range(nd_n)] for y in range(self.nPoints)]
    self.matrix_dNd_Eta = [[0 for x in range(nd_n)] for y in range(self.nPoints)]
    self.sides = [UniversalElementSide] * 4
    
    for i in range(self.nPoints):
      for j in range(nd_n):
        self.matrix_dNd_Ksi[i][j] = dN_dKsi(eta[i])[j]
        self.matrix_dNd_Eta[i][j] = dN_dEta(ksi[i])[j]

  def display(self):
    print('Matrix dN/dKsi')
    print_matrix(self.matrix_dNd_Ksi)
    print('Matrix dN/dEta')
    print_matrix(self.matrix_dNd_Eta)

