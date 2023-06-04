import max_solver
import min_solver


class IncorrectInput(Exception):
    pass


if __name__ == "__main__":

    with open("input.txt", "r") as input_file:
        problem = input_file.read().split("\n")
        if problem[0].split(" ")[0] == "MAX":
            max_solver.solve(5)
        elif problem[0].split(" ")[0] == "MIN":
            min_solver.solve(5)
        else:
            raise IncorrectInput
