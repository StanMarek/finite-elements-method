from math import sqrt
import numpy as np
from util.function import TWO_POINT_KEYS, dN_dEta, dN_dKsi, print_matrix, shape_function
from model.grid import Grid

eta = [TWO_POINT_KEYS[0], TWO_POINT_KEYS[0], TWO_POINT_KEYS[1], TWO_POINT_KEYS[1]]
ksi = [TWO_POINT_KEYS[0], TWO_POINT_KEYS[1], TWO_POINT_KEYS[1], TWO_POINT_KEYS[0]]
X = [0, 0.025, 0.025, 0]
Y = [0, 0, 0.025, 0.025]

"""
B - Bottom
R - Right
T - Top
L - Left
"""
element_side_border = {
  "B" : 0,
  "R" : 1,
  "T" : 2,
  "L" : 3,
}

def pithagorean_distance(x_1, x_2, y_1, y_2):
  x_diff = x_2 - x_1
  y_diff = y_2 - y_1
  return sqrt(
    pow(x_diff, 2) + pow(y_diff, 2) 
  )
class Point:
  def __init__(self, x, y, v):
    self.ksi = x
    self.eta = y
    self.weight = v
    self.N = [float] * 4

    for i in range(4):
      self.N[i] = shape_function(self.ksi, self.eta)[i]

class UniversalElementSide: 
  def __init__(self, n_points, side):
    self.number_of_ip = n_points
    self.side_id = side
    self.points = [Point] * self.number_of_ip
    
    if self.side_id == element_side_border["B"] or self.side_id == element_side_border["T"]:
      for i in range(n_points):
        self.points[i] = Point(
          x = TWO_POINT_KEYS[i],
          y = -1 if self.side_id == element_side_border["B"] else 1,
          v = 1
        )
    elif self.side_id == element_side_border["L"] or self.side_id == element_side_border["R"]:
      for i in range(n_points):
        self.points[i] = Point(
          x = -1 if self.side_id == element_side_border["L"] else 1,
          y = TWO_POINT_KEYS[i],
          v = 1
        )
    
    self.det_j = pithagorean_distance(
      self.points[0].ksi,
      self.points[1].ksi,
      self.points[0].eta,
      self.points[1].eta,
    )/2  
    
class UniversalElement:
  def __init__(self, number_of_points):
    nd_n = 4
    self.nPoints = number_of_points ** 2
    self.matrix_dNd_Ksi = [[0 for x in range(self.nPoints)] for y in range(self.nPoints)]
    self.matrix_dNd_Eta = [[0 for x in range(self.nPoints)] for y in range(self.nPoints)]
    self.sides = [UniversalElementSide] * 4
    
    for i in range(self.nPoints):
      for j in range(nd_n):
        self.matrix_dNd_Ksi[i][j] = dN_dKsi(eta[i])[j]
        self.matrix_dNd_Eta[i][j] = dN_dEta(ksi[i])[j]

    for i in range(4):
      self.sides = UniversalElementSide(number_of_points, i)

  def display(self):
    print('Matrix dN/dKsi')
    print_matrix(self.matrix_dNd_Ksi)
    print('Matrix dN/dEta')
    print_matrix(self.matrix_dNd_Eta)

