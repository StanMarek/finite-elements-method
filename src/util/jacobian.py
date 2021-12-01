from model.grid import Grid
from model.universal_element import X, Y, UniversalElement


def jacobian(nOfElem, nOfIP, e42d: UniversalElement, grid: Grid):
  dXdKsi = 0.0
  dYdEta = 0.0
  dXdEta = 0.0
  dYdKsi = 0.0

  for j in range(4):
    # dev
    nodeId = grid.elements[nOfElem].ID[j] - 1
    dXdKsi += e42d.matrix_dNd_Ksi[nOfIP][j] * grid.nodes[nodeId].x
    dYdEta += e42d.matrix_dNd_Eta[nOfIP][j] * grid.nodes[nodeId].y
    dXdEta += e42d.matrix_dNd_Eta[nOfIP][j] * grid.nodes[nodeId].x
    dYdKsi += e42d.matrix_dNd_Ksi[nOfIP][j] * grid.nodes[nodeId].y
    # test
    # dXdKsi += e42d.matrix_dNd_Ksi[nOfIP][j] * X[j]
    # dYdEta += e42d.matrix_dNd_Eta[nOfIP][j] * Y[j] 

  J = [[0 for y in range(2)] for x in range(2)]
  transpose_j = [[0 for y in range(2)] for x in range(2)]
  J[0][0] = dXdKsi
  J[0][1] = dYdKsi
  J[1][0] = dXdEta
  J[1][1] = dYdEta

  det_j = (J[0][0] * J[1][1]) - (J[0][1] * J[1][0])
  inverse_det_j = 1/det_j

  transpose_j[0][0] = J[1][1]
  transpose_j[0][1] = - J[0][1]
  transpose_j[1][0] = - J[1][0]
  transpose_j[1][1] = J[0][0]
  
  for i in range(2):
    for j in range(2):
      J[i][j] = inverse_det_j * transpose_j[i][j]

  return J, det_j