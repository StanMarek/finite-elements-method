import numpy as np
from model.universal_element import element_side_border
from util.function import pithagorean_distance


class Element:
    """Element class
    Represents set of 4 nodes with their IDs.
    Used to calculate global matrices used in simulation.
    Element has 4 sides and can be any rectangular shape

    Attributes:
    - ID - ids of 4 nodes
    - H - h matrix
    - H_bc - h boundary condidtion matrix
    - P - p vector - load vector - wektor obciążeń
    - C - c matrix  
    """
    def __init__(self, id):
        self.ID = id
        self.H = np.zeros((4, 4))
        self.H_bc = np.zeros((4, 4))
        self.P = np.zeros(4)
        self.C = np.zeros((4, 4))

    def set_H(self, H):
        self.H = H

    def set_C(self, C):
        self.C = C

    def set_Hbc(self, Hbc):
        self.H_bc = Hbc

    def set_P(self, P):
        self.P = P

    def __str__(self) -> str:
        return str(f"id1={self.ID[0]} id2={self.ID[1]} id3={self.ID[2]} id4={self.ID[3]}")

    def check_element_boundary_condition(self, grid):

        side_det_j = np.zeros(4)
        side_choice = np.zeros(4)

        if (grid.nodes[self.ID[0]-1].bc == 1 and
                grid.nodes[self.ID[1]-1].bc == 1):
            side_choice[element_side_border["B"]] = 1
            side_det_j[element_side_border["B"]] = pithagorean_distance(
                grid.nodes[self.ID[0]-1].x,
                grid.nodes[self.ID[1]-1].x,
                grid.nodes[self.ID[0]-1].y,
                grid.nodes[self.ID[1]-1].y
            )/2

        if (grid.nodes[self.ID[1]-1].bc == 1 and
                grid.nodes[self.ID[2]-1].bc == 1):
            side_choice[element_side_border["R"]] = 1
            side_det_j[element_side_border["R"]] = pithagorean_distance(
                grid.nodes[self.ID[1]-1].x,
                grid.nodes[self.ID[2]-1].x,
                grid.nodes[self.ID[1]-1].y,
                grid.nodes[self.ID[2]-1].y
            )/2

        if (grid.nodes[self.ID[2]-1].bc == 1 and
                grid.nodes[self.ID[3]-1].bc == 1):
            side_choice[element_side_border["T"]] = 1
            side_det_j[element_side_border["T"]] = pithagorean_distance(
                grid.nodes[self.ID[2]-1].x,
                grid.nodes[self.ID[3]-1].x,
                grid.nodes[self.ID[2]-1].y,
                grid.nodes[self.ID[3]-1].y
            )/2

        if (grid.nodes[self.ID[0]-1].bc == 1 and
                grid.nodes[self.ID[3]-1].bc == 1):
            side_choice[element_side_border["L"]] = 1
            side_det_j[element_side_border["L"]] = pithagorean_distance(
                grid.nodes[self.ID[0]-1].x,
                grid.nodes[self.ID[3]-1].x,
                grid.nodes[self.ID[0]-1].y,
                grid.nodes[self.ID[3]-1].y
            )/2

        return side_det_j, side_choice


