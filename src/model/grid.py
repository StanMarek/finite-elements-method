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

    def display(self):
        s = """
		GRID values:
		Height: {}, Width: {}
		NoNodes: {}, NoElems: {}
		dX: {:.3f}, dY: {:.3f}
		"""
        print(s.format(self.H, self.B, self.nN,
              self.nE, self.delta_x, self.delta_y))

        # print nodes
        for node in range(len(self.nodes)):
            print(f"NodeNr:{node+1}\t", self.nodes[node])

        # print elements
        for element in range(len(self.elements)):
            print(f"ElemNr:{element+1}\t", self.elements[element])

        columns = self.nB - 1
        rows = self.nH - 1
        unit = 5
        el_id = 0
        last_elem_in_column = rows - 1
        rows_start = 0
        print("B, H " + "-" * 10 + ">")
        print("|\n" * 4 + "v")

        for _ in range(columns):
            for r in range(rows):
                print(('\033[91m'+"{}".format(self.elements[el_id +
                      r].ID[0]) + '\033[0m' + "- " * unit), end='')
            print(
                '\033[91m' + "{}".format(self.elements[last_elem_in_column].ID[3]) + '\033[0m')

            for j in range(unit):
                if j == (int)(unit/2):
                    for c in range(rows_start, columns + 1 + rows_start, 1):
                        print("|" + "  " * int(unit / 2) +
                              "{}".format(c + 1) + "  " * int(unit / 2), end="")
                    rows_start += rows
                print(("|" + "  " * unit) * rows + "|")

            el_id += rows
            last_elem_in_column += rows
        for r in range(rows):
            last_column = (self.nH - 1) * (self.nB - 1) - rows + r
            print(('\033[91m' + "{}".format(self.elements[last_column].ID[1]
                                            ) + '\033[0m' + "- " * unit), end='')
        print('\033[91m' +
              "{}".format(self.elements[self.nE - 1].ID[2]) + '\033[0m')
