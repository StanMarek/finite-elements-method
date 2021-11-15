from model.element import Element
from model.element4_2D import *
from model.grid import Grid
from model.node import Node
from util.function import gauss_1dim, gauss_2dim

def main():
	grid = Grid(0.2, 0.1, 5, 4)
	grid.display()
	
	el = Element4_2D(4)
	el.display()

	
	for elementNumber in range(grid.nE):
		for integrationPoint in range(el.nPoints):
			jac = jacobian(elementNumber, integrationPoint, el, grid)

	H = calculateHMatrixForElem(el, jac, 0.000156, 30)
	printMatrix(H)

if __name__ == '__main__':
	main()