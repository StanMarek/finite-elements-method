from model.element import Element
from model.element4_2D import Element4_2D
from model.grid import GRID
from model.node import Node
from util.function import gauss_1dim, gauss_2dim

def main():
    # grid = GRID(0.2, 0.1, 5, 4)
    # grid.display()
    # print(gauss_1dim(2))
    # print(gauss_1dim(3))
    # print(gauss_2dim(2))
    # print(gauss_2dim(3))
    el = Element4_2D(2)
    el.print()

    
if __name__ == '__main__':
    main()