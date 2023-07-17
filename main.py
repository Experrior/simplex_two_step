import max_solver
import min_solver
import sys, os

class IncorrectInput(Exception):
    pass


if __name__ == "__main__":
    verbose = True
    sys.stdout = open(os.devnull, 'w')
    if verbose: sys.stdout = sys.__stdout__

    with open("input.txt", "r") as input_file:
        problem = input_file.read().split("\n")
        if problem[0].split(" ")[0].lower() == "max":
            output = max_solver.solve(5)
        elif problem[0].split(" ")[0].lower() == "min":
            output = min_solver.solve(5)
        else:
            raise IncorrectInput
