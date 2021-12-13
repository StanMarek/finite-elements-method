from model.element import Element
from model.node import Node
from util.const import T_INIT


class Grid:

    def __init__(self, H, B, nH, nB):
        self.H = H
        self.B = B
        self.nH = nH
        self.nB = nB
        self.nN = nH * nB
        self.nE = (nH-1)*(nB-1)
        self.nodes = [Node]*self.nN
        self.elements = [Element]*self.nE
        self.delta_x = B / (nB - 1)
        self.delta_y = H / (nH - 1)

        node = 0
        for x in range(nB):
            for y in range(nH):
                self.nodes[node] = Node(x * self.delta_x, y * self.delta_y)
                node += 1

        for i in range(self.nN):
            if self.nodes[i].x == 0 or self.nodes[i].x == B:
                self.nodes[i].set_bc(1)
            if self.nodes[i].y == 0 or self.nodes[i].y == H:
                self.nodes[i].set_bc(1)
            self.nodes[i].t = T_INIT

        next = 1
        for i in range(len(self.elements)):
            if next % nH == 0:
                next += 1
            id1 = next
            id2 = nH + id1
            id3 = id2 + 1
            id4 = id1 + 1
            ids = [id1, id2, id3, id4]
            self.elements[i] = Element(ids)
            next += 1
