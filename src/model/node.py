
from util.const import T_INIT


class Node:
    """Node class
    Represents the most basic thing to caculate heat/thermal
    distribution in project

    Attributes:
    - x 
    - y
    - bc - boundary condidtion
    - t - temperature
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bc = 0
        self.t = T_INIT

    def set_bc(self, bc):
        self.bc = bc

    def set_t(self, t):
        self.t = t

    def __repr__(self) -> str:
        return f"x:{self.x}\ty:{self.y}\tbc:{self.bc}\tt:{self.t}"
