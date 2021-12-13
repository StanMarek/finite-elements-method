from termcolor import colored
from model.grid import Grid
from model.universal_element import UniversalElement
from simulation import simulation


def main() -> None:

    grid = Grid(0.1, 0.1, 4, 4)

    SCHEMA = 2
    element = UniversalElement(SCHEMA)

    print(colored("Liczba punktów całkowania:", "magenta"), SCHEMA)
    simulation(grid, element)
    

if __name__ == '__main__':
    main()
