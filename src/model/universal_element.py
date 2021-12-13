import numpy as np

from util.const import THREE_POINT_KEYS, THREE_POINT_VALUES, TWO_POINT_KEYS, TWO_POINT_VALUES
from util.function import (dN_dEta, dN_dKsi, print_matrix,
                               shape_function)

eta = [TWO_POINT_KEYS[0], TWO_POINT_KEYS[0],
       TWO_POINT_KEYS[1], TWO_POINT_KEYS[1]]
ksi = [TWO_POINT_KEYS[0], TWO_POINT_KEYS[1],
       TWO_POINT_KEYS[1], TWO_POINT_KEYS[0]]
# X = [0, 0.025, 0.025, 0]
# Y = [0, 0, 0.025, 0.025]

"""
B - Bottom
R - Right
T - Top
L - Left
"""
element_side_border = {
    "B": 0,
    "R": 1,
    "T": 2,
    "L": 3,
}


class Point:
    def __init__(self, x, y, v):
        self.ksi = x
        self.eta = y
        self.weight = v
        self.N = [float] * 4

        for i in range(4):
            self.N[i] = shape_function(self.ksi, self.eta)[i]
        # print("Point from UE - N:", self.N)
        # print("Point from UE - ksi:", self.ksi)
        # print("Point from UE - eta:", self.eta)
        # print("Point from UE - w:", self.weight)

    def __str__(self) -> str:
        return str(f"ksi={self.ksi} eta={self.eta} w={self.weight}")



class UniversalElementSide:
    def __init__(self, n_points, side):
        self.number_of_ip = n_points
        self.side_id = side
        self.points = [Point] * self.number_of_ip

        if self.number_of_ip == 2:

            if self.side_id == element_side_border["B"] or self.side_id == element_side_border["T"]:
                for i in range(self.number_of_ip):
                    self.points[i] = Point(
                        x = TWO_POINT_KEYS[i],
                        y = -1 if self.side_id == element_side_border["B"] else 1,
                        v = 1
                    )
            elif self.side_id == element_side_border["L"] or self.side_id == element_side_border["R"]:
                for i in range(self.number_of_ip):
                    self.points[i] = Point(
                        x = -1 if self.side_id == element_side_border["L"] else 1,
                        y = TWO_POINT_KEYS[i],
                        v = 1
                    )

        elif self.number_of_ip == 3:

            if self.side_id == element_side_border["B"] or self.side_id == element_side_border["T"]:
                for i in range(self.number_of_ip):
                    self.points[i] = Point(
                        x = THREE_POINT_KEYS[i],
                        y = -1 if self.side_id == element_side_border["B"] else 1,
                        v = THREE_POINT_VALUES[0] if i != 1 else THREE_POINT_VALUES[1]
                    )

            elif self.side_id == element_side_border["L"] or self.side_id == element_side_border["R"]:
                for i in range(self.number_of_ip):
                    self.points[i] = Point(
                        x = -1 if self.side_id == element_side_border["L"] else 1,
                        y = THREE_POINT_KEYS[i],
                        v = THREE_POINT_VALUES[0] if i != 1 else THREE_POINT_VALUES[1]
                    )
    

class UniversalElement:

    def __init__(self, number_of_points):

        self.nPoints = number_of_points ** 2
        self.matrix_dN_dKsi = np.zeros((self.nPoints, 4))
        self.matrix_dN_dEta = np.zeros((self.nPoints, 4))
        self.sides = [UniversalElementSide] * 4
        self.points = [Point] * self.nPoints

        for i in range(4):
            self.sides[i] = UniversalElementSide(number_of_points, i)


        if number_of_points == 2:

            eta = [TWO_POINT_KEYS[0], TWO_POINT_KEYS[0],
                   TWO_POINT_KEYS[1], TWO_POINT_KEYS[1]]


            ksi = [TWO_POINT_KEYS[0], TWO_POINT_KEYS[1],
                TWO_POINT_KEYS[1], TWO_POINT_KEYS[0]]
        
            for i in range(self.nPoints):
                for j in range(4):
                    self.matrix_dN_dKsi[i][j] = dN_dKsi(eta[i])[j]
                    self.matrix_dN_dEta[i][j] = dN_dEta(ksi[i])[j]

            self.points[0] = Point(TWO_POINT_KEYS[0], TWO_POINT_KEYS[0], TWO_POINT_VALUES[0])
            self.points[1] = Point(TWO_POINT_KEYS[1], TWO_POINT_KEYS[0], TWO_POINT_VALUES[0])
            self.points[2] = Point(TWO_POINT_KEYS[1], TWO_POINT_KEYS[1], TWO_POINT_VALUES[0])
            self.points[3] = Point(TWO_POINT_KEYS[0], TWO_POINT_KEYS[1], TWO_POINT_VALUES[0])

        elif number_of_points == 3:

            eta = [THREE_POINT_KEYS[0], THREE_POINT_KEYS[0], THREE_POINT_KEYS[2],
                   THREE_POINT_KEYS[2], THREE_POINT_KEYS[0], THREE_POINT_KEYS[1],
                   THREE_POINT_KEYS[2], THREE_POINT_KEYS[1], THREE_POINT_KEYS[1]]

            ksi = [THREE_POINT_KEYS[0], THREE_POINT_KEYS[2], THREE_POINT_KEYS[2],
                   THREE_POINT_KEYS[0], THREE_POINT_KEYS[1], THREE_POINT_KEYS[2],
                   THREE_POINT_KEYS[1], THREE_POINT_KEYS[0], THREE_POINT_KEYS[1]]

            for i in range(self.nPoints):
                for j in range(4):
                    self.matrix_dN_dKsi[i][j] = dN_dKsi(eta[i])[j]
                    self.matrix_dN_dEta[i][j] = dN_dEta(ksi[i])[j]

            self.points[0] = Point(THREE_POINT_KEYS[0], THREE_POINT_KEYS[0], THREE_POINT_VALUES[0])
            self.points[1] = Point(THREE_POINT_KEYS[2], THREE_POINT_KEYS[0], THREE_POINT_VALUES[2])
            self.points[2] = Point(THREE_POINT_KEYS[2], THREE_POINT_KEYS[2], THREE_POINT_VALUES[2])
            self.points[3] = Point(THREE_POINT_KEYS[0], THREE_POINT_KEYS[0], THREE_POINT_VALUES[0])
            self.points[4] = Point(THREE_POINT_KEYS[1], THREE_POINT_KEYS[0], THREE_POINT_VALUES[1])
            self.points[5] = Point(THREE_POINT_KEYS[2], THREE_POINT_KEYS[1], THREE_POINT_VALUES[1])
            self.points[6] = Point(THREE_POINT_KEYS[1], THREE_POINT_KEYS[2], THREE_POINT_VALUES[1])
            self.points[7] = Point(THREE_POINT_KEYS[0], THREE_POINT_KEYS[1], THREE_POINT_VALUES[1])
            self.points[8] = Point(THREE_POINT_KEYS[1], THREE_POINT_KEYS[1], THREE_POINT_VALUES[1])


    def display(self):

        print('Matrix dN/dKsi')
        print_matrix(self.matrix_dN_dKsi)
        print('Matrix dN/dEta')
        print_matrix(self.matrix_dN_dEta)
