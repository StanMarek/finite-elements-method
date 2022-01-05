from os import sep
import numpy as np
from numpy.lib.shape_base import split
from model.element import Element
from model.node import Node
from util.const import T_INIT


class Grid:
    """Grid model
    Represents wholse set/net of elements and nodes
    used to caalculate heat distribution. Currently
    interpreted as rectangular shape
    
    Attributes:
    - H - height of grid
    - B - width of grid
    - nH - number of nodes in side walls,
        number of nodes in H direction
    - nB - number of nodes in top/bottom walls,
        number of nodes in B direction
    - nN - number of nodes in this grid
    - nE - number of elemenents in this grid 
    - nodes - array of Nodes, size is nN
    - elements - array of Elements, size is nE 
    """
    # def __init__(self, H, B, nH, nB):
    def __init__(self, *args):

        if len(args) > 1:
            self.H = args[0]
            self.B = args[1]
            self.nH = args[2]
            self.nB = args[3]
            self.nN = self.nH * self.nB
            self.nE = (self.nH-1)*(self.nB-1)
            self.nodes = [Node]*int(self.nN)
            self.elements = [Element]*self.nE

            delta_x = self.B / (self.nB - 1)
            delta_y = self.H / (self.nH - 1)

            node = 0
            for x in range(self.nB):
                for y in range(self.nH):
                    self.nodes[node] = Node(x * delta_x, y * delta_y)
                    node += 1

            for i in range(self.nN):
                if self.nodes[i].x == 0 or self.nodes[i].x == self.B:
                    self.nodes[i].set_bc(1)
                if self.nodes[i].y == 0 or self.nodes[i].y == self.H:
                    self.nodes[i].set_bc(1)

            next = 1
            for i in range(len(self.elements)):
                if next % self.nH == 0:
                    next += 1
                id1 = next
                id2 = self.nH + id1
                id3 = id2 + 1
                id4 = id1 + 1
                ids = [id1, id2, id3, id4]
                self.elements[i] = Element(ids)
                next += 1
            
        else:
            with open(args[0]) as f:
                lines = f.readlines()

            nodes_index = 0
            elements_index = 0
            bc_index = 0
            
            split = []
            for line in lines:
                split.append(line.split())
            
            for i in range(len(split)):
                # print(split[i][0])
                if split[i][0] == "*Node" or split[i][0] == "*Node,":
                    nodes_index = i
                if split[i][0] == "*Element" or split[i][0] == "*Element,":
                    elements_index = i
                if split[i][0] == "*BC" or split[i][0] == "*BC,":
                    bc_index = i

            nodes = split[nodes_index + 1:elements_index]
            elements = split[elements_index + 1:bc_index]
            condition = split[bc_index + 1:]
            condition = np.reshape(condition, len(condition[0]))
            

            for i in range(len(nodes)):
                for j in range(len(nodes[i])):
                    if nodes[i][j][len(nodes[i][j]) - 1] == ",":
                        nodes[i][j] = nodes[i][j][:-1] 
                    nodes[i][j] = float(nodes[i][j])
                    nodes[i][0] = int(nodes[i][0])

            for i in range(len(elements)):
                for j in range(len(elements[i])):
                    if elements[i][j][len(elements[i][j]) - 1] == ",":
                        elements[i][j] = elements[i][j][:-1]
                    elements[i][j] = int(elements[i][j])

            for i in range(len(condition)):
                if condition[i][len(condition[i]) - 1] == ",":
                    condition[i] = condition[i][:-1]
                condition[i] = int(condition[i])
                

            self.nN = len(nodes)
            self.nE = len(elements)
            self.nodes = [Node]*int(self.nN)
            self.elements = [Element]*self.nE

            for node in nodes:
                id = node[0] - 1
                x = node[1]
                y = node[2]
                self.nodes[id] = Node(x, y)
                # print(self.nodes[id])
            
            for bc in condition:
                node = int(bc) - 1
                self.nodes[node].set_bc(1)

            for element in elements:
                id = element[0] - 1
                ids = element[1:]
                id1 = ids[2]
                id2 = ids[3]
                id3 = ids[0]
                id4 = ids[1]
                ids = [id1, id2, id3, id4]
                self.elements[id] = Element(ids)

                # print(self.elements[id])

    def __repr__(self) -> str:
        return "\n".join("{}".format(node) for node in enumerate(self.nodes)) + "\n" + "\n".join("{}".format(element) for element in enumerate(self.elements))

    # @classmethod
    # def from_dictionary(cls, datadict):
    #     return cls(datadict.items())


    # @classmethod
    # def from_file(cls, filename):
    #     data = open(filename).readlines()
    #     return cls(data)

