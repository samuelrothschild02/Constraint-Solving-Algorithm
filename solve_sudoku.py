# Sam Rothschild 24/10/23
# sudoku assignment
# test SAT class
from display import display_sudoku_solution
import random, sys
from SAT import SAT

THRESHOLD = 0.8
MAX_ITS = 100000

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)
    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])

    # result = sat.GSAT(THRESHOLD, MAX_ITS)
    result = sat.walkSAT(THRESHOLD, MAX_ITS)
    # result = sat.solve_with_resolution()

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
