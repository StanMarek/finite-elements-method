from model.element import Element
from model.element4_2D import Element4_2D, jacobian
from model.grid import Grid
from model.node import Node
from util.function import gauss_1dim, gauss_2dim

def main():
	grid = Grid(0.2, 0.1, 5, 4)
	grid.display()
	
	el = Element4_2D(4)
	el.display()

	for i in range(grid.nE):
		for j in range(el.nPoints):
			jacobian(i, j, el, grid)

if __name__ == '__main__':
	main()