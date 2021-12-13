
class Node:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bc = 0
        self.t = 0

    def set_bc(self, bc):
        self.bc = bc

    def set_t(self, t):
        self.t = t

    def __str__(self) -> str:
        return str("x={:.3f} y={:.3f} bc={}".format(self.x, self.y, self.bc))
