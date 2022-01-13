from termcolor import colored
from model.grid import Grid
from model.universal_element import UniversalElement
from simulation import simulation
import time


def main() -> None:

    grid = Grid(0.1, 0.1, 4, 4)
    # grid = Grid("init_1_4x4.txt")
    # grid = Grid("init_2_4x4.txt")
    # grid = Grid("init_3_31x31.txt")
    # grid = Grid("init_4_31x31.txt")
    # grid = Grid(0.1, 0.1, 31, 31)

    SCHEMA = 3
    element = UniversalElement(SCHEMA)

    print(colored("Liczba punktów całkowania:", "magenta"), SCHEMA)
    t = time.perf_counter()
    simulation(grid, element)
    t = time.perf_counter() - t
    print("Czas symulacji:", t)


if __name__ == '__main__':

    main()
