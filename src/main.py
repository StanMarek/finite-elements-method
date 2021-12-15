from termcolor import colored
from model.grid import Grid
from model.universal_element import UniversalElement
from simulation import simulation
import time

def main() -> None:

    grid = Grid(0.1, 0.1, 4, 4)
    # grid = Grid(0.1, 0.1, 31, 31)

    SCHEMA = 2
    element = UniversalElement(SCHEMA)

    print(colored("Liczba punktów całkowania:", "magenta"), SCHEMA)
    t = time.time()
    simulation(grid, element)
    t = time.time() - t
    print("Czas symulacji:", t) 

    grid = Grid(0.1, 0.1, 4, 4)

    SCHEMA = 3
    element = UniversalElement(SCHEMA)

    print(colored("Liczba punktów całkowania:", "magenta"), SCHEMA)
    t = time.time()
    simulation(grid, element)
    t = time.time() - t
    print("Czas symulacji:", t) 


if __name__ == '__main__':

    main()
