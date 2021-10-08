from model.element import Element
from model.node import Node

class GRID:
	def __init__(self, H, B, nH, nB):
		self.H = H
		self.B = B
		self.nH = nH
		self.nB = nB
		self.nN = nH * nB
		self.nE = (nH-1)*(nB-1)
		self.nodes = [Node]*self.nN
		self.elements = [Element]*self.nE
		
		deltaX = B/(nB-1)
		deltaY = H/(nH-1)

		for i in range(nB):
			for j in range(nH):
				self.nodes[i].x = i * deltaX
				self.nodes[i].y = j * deltaY

		alfa = 0
		for i in range(1, self.nE):
			if(i % 4 == 0):
				alfa += 1
				
			self.elements[i].ID[0] = i + alfa
			self.elements[i].ID[1] = self.nodes[i].ID[0] + nH
			self.elements[i].ID[2] = self.nodes[i].ID[1] + 1
			self.elements[i].ID[3] = self.nodes[i].ID[0] + 1

	def print(self):
		s = """
		GRID values:
		Height: {}, Width: {}
		NoNodes: {}, NoElems: {}
		"""
		print(s.format(self.H, self.B, self.nN, self.nE))

		for i in range(len(self.nodes)):
			print("x={:.2f} y={:.2f}".format(self.nodes[i].x, self.nodes[i].y))
		
		for i in range(len(self.elements)):
			print("ID1={} ID12={} ID3={} ID4={}".format(self.elements[i].ID[0], self.elements[i].ID[1], self.elements[i].ID[2], self.elements[i].ID[3]))
