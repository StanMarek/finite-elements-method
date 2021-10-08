from model.element import Element
from model.grid import GRID
from model.node import Node


def main():
    grid = GRID(0.2, 0.1, 5, 4)
    grid.print()

    return

if __name__ == '__main__':
    main()