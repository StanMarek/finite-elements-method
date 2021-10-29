from model.element import Element
from model.node import Node

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
		self.deltaX = B/(nB-1)
		self.deltaY = H/(nH-1)

		node = 0
		for x in range(nB):
			for y in range(nH):
				self.nodes[node] = Node(x * self.deltaX, y * self.deltaY)
				node += 1

		next = 1
		for i in range(len(self.elements)):
			if next % nH == 0:
				next += 1
			
			ID1 = next
			ID2 = nH + ID1 
			ID3 = ID2 + 1
			ID4 = ID1 + 1
			ids = [ID1, ID2, ID3, ID4]
			self.elements[i] = Element(ids)
			next += 1
		
	
	def display(self):
		s = """
		GRID values:
		Height: {}, Width: {}
		NoNodes: {}, NoElems: {}
		dX: {:.3f}, dY: {:.3f}
		"""
		print(s.format(self.H, self.B, self.nN, self.nE, self.deltaX, self.deltaY))

		# print nodes
		for node in range(len(self.nodes)):
			print(f"NodeNr:{node+1}\t", self.nodes[node])

		# print elements
		for element in range(len(self.elements)):
			print(f"ElemNr:{element+1}\t", self.elements[element])
		