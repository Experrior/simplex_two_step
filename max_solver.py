from printer import print_simplex
import sys


class NoAnswer(Exception):
    pass


class NoFeasibleSolution(Exception):
    pass


class NoLoopingDetected(Exception):
    pass


class UnboundedSolution(Exception):
    pass


def is_looping(seen):
    """
        Helper function to check if simplex is looping through finite solution set.
        :param seen: List of pairs: (column, row)
        :return: boolean True if there's a loop in a list
    """
    last = seen[0]
    last_inx = 0
    streak = 0
    wait = 3
    solution = []
    for i in range(len(seen)):
        if last == seen[i] and last_inx != i:
            streak += 1
            last_inx += 1
            last = seen[last_inx]
        elif wait == 0:
            wait = 3
            for j in range(i):
                if seen[j] == seen[i]:
                    streak = 0
                    last_inx = j
                    last = seen[last_inx]
                    break
        else:
            wait -= 1
        if streak > 5:
            solution.append(last)
            last = seen[last_inx + 1]

    if len(solution) > 0:
        return True, solution
    raise NoLoopingDetected


def solve_basic(simplex_tableau, maximize, basic_variables):
    a = 0
    size = len(simplex_tableau) - 1
    seen = []
    force_end = False
    while not force_end:
        print_simplex(simplex_tableau)

        # find pivot column
        pivot_column = -1
        column_count = 0

        if maximize:  # choosing the largest negative
            temp = 1
            for i in range(size):
                if temp >= 0:
                    temp = simplex_tableau[i][-1]
                if simplex_tableau[i][-1] <= temp and simplex_tableau[i][-1] < 0:
                    column_count += 1
                    pivot_column = i
                    temp = simplex_tableau[i][-1]
        else:  # choosing the smallest positive
            temp = -1
            for i in range(size):
                if temp <= 0:
                    temp = simplex_tableau[i][-1]
                if simplex_tableau[i][-1] >= temp and simplex_tableau[i][-1] > 0:
                    column_count += 1
                    pivot_column = i
                    temp = simplex_tableau[i][-1]

        # find pivot row
        if pivot_column == -1:
            return simplex_tableau, "finished", basic_variables

        pivot_row = -1

        ratio = 0
        for i in range(len(simplex_tableau[0]) - 1):
            # if simplex_tableau[pivot_column][i] <= 0: continue
            if ratio <= 0 and simplex_tableau[pivot_column][i] != 0:
                ratio = simplex_tableau[-1][i] / simplex_tableau[pivot_column][i]
            if simplex_tableau[pivot_column][i] != 0 and 0 < simplex_tableau[-1][i] / simplex_tableau[pivot_column][
                i] <= ratio:
                pivot_row = i
                ratio = simplex_tableau[-1][i] / simplex_tableau[pivot_column][i]

        if pivot_row == -1 and column_count >= 1:
            return simplex_tableau, "unbounded", basic_variables

        if pivot_row == -1:
            return simplex_tableau, "finished", basic_variables

        seen.append((pivot_column, pivot_row))
        basic_variables[pivot_row] = pivot_column

        if a > 100:
            _, finish = is_looping(seen)
            final = [-1] * (len(finish))

            for i in range(len(finish)):
                final[i] = simplex_tableau[-1][finish[i][1]] / simplex_tableau[finish[i][0]][finish[i][1]]
            force_end = True
            final.sort()
            for i in range(len(final)):
                if final[i] <= 0:
                    continue
                else:
                    pivot_column, pivot_row = finish[i][0], finish[i][1]
                    break

        number = simplex_tableau[pivot_column][pivot_row]
        for i in range(len(simplex_tableau)):
            simplex_tableau[i][pivot_row] /= number

        #  solve for given pivot
        for i in range(len(simplex_tableau[pivot_column])):
            number = -simplex_tableau[pivot_column][i]
            if i == pivot_row or number == 0: continue
            for j in range(len(simplex_tableau)):
                simplex_tableau[j][i] += (number * simplex_tableau[j][pivot_row])

            print_simplex(simplex_tableau)

        a += 1
        print([pivot_column, pivot_row])
    return simplex_tableau, "finished", basic_variables


def solve(bound) -> None:
    """
        Main function for solving linear maximization problem.
        :param bound: Parameter for round() function for printing float numbers
        :return: None
    """

    # read and save input data into ram
    with open("input.txt", "r") as input_file:
        problem = input_file.read().split("\n")

        num_of_variables = 0
        num_of_constraints = 0
        optimization = []
        constraints = []
        values = []

        for i in problem[0].split(" ")[1:]:
            num_of_variables += 1
            optimization.append(i)
        orig_variables = num_of_variables
        k = 1
        while k < len(problem):
            constraints.append(problem[k].split(" "))
            if float(constraints[-1][-1]) == 0.0:
                values.append(sys.float_info.min)
            else:
                values.append(float(constraints[-1][-1]))
            k += 1
            num_of_constraints += 1

    # for all the constraints transform them, and add artificial,extensive,slug variables:
    slug = [0] * num_of_constraints
    extensive = [0] * num_of_constraints
    artificial = [0] * num_of_constraints

    no_slug = 0
    no_extensive = 0
    no_artificial = 0

    # fill the number of variables according to equality/inequality
    for i in range(num_of_constraints):
        match constraints[i][-2]:
            case "<":
                slug[i] = 1
                no_slug += 1
            case "=":
                artificial[i] = 1
                no_artificial += 1
            case ">":
                extensive[i] = -1
                no_extensive += 1
                artificial[i] = 1
                no_artificial += 1

    # create initial simplex tableau for phase 1

    # add variable columns
    simplex_tableau = []
    for i in range(num_of_variables):
        temp_var = [float(x[i]) for x in constraints]
        temp_var.append(0)
        simplex_tableau.append(temp_var)

    # add slug columns
    for i in range(num_of_constraints):
        temp_var = [0] * (num_of_constraints + 1)
        if slug[i] != 0:
            temp_var[i] = slug[i]
            simplex_tableau.append(temp_var)

    # add extensive columns
    for i in range(num_of_constraints):
        temp_var = [0] * (num_of_constraints + 1)
        if extensive[i] != 0:
            temp_var[i] = extensive[i]
            simplex_tableau.append(temp_var)

    # add artificial columns
    for i in range(num_of_constraints):
        temp_var = [0] * (num_of_constraints + 1)
        if artificial[i] != 0:
            temp_var[i] = artificial[i]
            temp_var[-1] = -artificial[i]
            simplex_tableau.append(temp_var)

    print_simplex(simplex_tableau)

    # add values column
    values.append(0)
    simplex_tableau.append(values)

    basic_variables = [-1] * len(simplex_tableau[0])

    # --- phase 1 ---

    # remove artificial variables from objective row
    target_row = 0
    for i in range(no_artificial):
        for j in range(len(simplex_tableau[0])):
            if simplex_tableau[-2 - i][j] != 0:
                target_row = j
                break
        for k in range(len(simplex_tableau)):
            simplex_tableau[k][-1] += simplex_tableau[k][target_row]

    print_simplex(simplex_tableau)
    print("\n", num_of_variables, no_slug, no_extensive, no_artificial)

    # solve for normal variables:
    simplex_tableau, message, basic_variables = solve_basic(simplex_tableau, False, basic_variables)

    print_simplex(simplex_tableau)
    print(num_of_variables, no_slug, no_extensive, no_artificial, "\n\n End of phase 1 \n")

    # check case 1:
    if round(simplex_tableau[-1][-1], 4) > 0:
        print("No feasible solution exists\n\n")
    else:

        # remove all artificial columns
        simplex_tableau = simplex_tableau[0:-no_artificial - 1] + [simplex_tableau[-1]]
        no_artificial = 0

        print_simplex(simplex_tableau)
        print(num_of_variables, no_slug, no_extensive, no_artificial, "\n\n\n")

        # check case 3

        # see if there are any negative x's in objective row, if so delete them
        to_delete = []
        for i in range(num_of_variables):
            if simplex_tableau[i][-1] < 0:
                to_delete.append(i)

        # plug in original objective function
        for i in range(num_of_variables):
            simplex_tableau[i][-1] = -float(optimization[i])

        # delete non basic x's
        for i in to_delete:
            del simplex_tableau[i]
            num_of_variables -= 1

        print_simplex(simplex_tableau)
        print(num_of_variables, no_slug, no_extensive, no_artificial, "\n\n\n")

        simplex_tableau, message, basic_variables = solve_basic(simplex_tableau, True, basic_variables)

        print_simplex(simplex_tableau)




        # analyze the final simplex matrix
        tab = []
        for i in range(num_of_variables):
            found = False
            for j in range(len(simplex_tableau[i])):
                if simplex_tableau[i][j] == 1 and found:
                    found = False
                    tab.pop()
                    break
                if simplex_tableau[i][j] == 1:
                    found = True
                    tab.append((i, j))
                if simplex_tableau[i][j] != 1 and simplex_tableau[i][j] != 0:
                    if found: tab.pop()
                    found = False
                    break

        solutions = []
        for i in tab:
            solutions.append(i[0] + 1)

        # update variable numbers with respect to deleted columns
        for iterator in to_delete:
            for i in range(len(solutions)):
                if solutions[i] >= iterator:
                    solutions[i] += 1
            for i in range(len(basic_variables)):
                if basic_variables[i] != -1 and basic_variables[i] >= iterator:
                    basic_variables[i] += 1

        if message == "unbounded":
            print("Solution unbounded")

        # fs ~ storage for deriving variables values
        fs = {}

        for i in range(len(basic_variables)):
            if basic_variables[i] != -1:
                fs[basic_variables[i] + 1] = simplex_tableau[-1][i]

        for i in range(len(basic_variables)):
            if basic_variables[i] != -1:
                for k in solutions:
                    if k - 1 == basic_variables[i]:
                        fs[k] = simplex_tableau[-1][i]

        # search constraints to derive the remaining variables:
        final_solution = {}
        for constraint in constraints:
            if constraint[-2] == "=" or constraint[-2] == "<":
                sum = 0
                for k in fs.keys():
                    if k <= orig_variables:
                        sum += float(constraint[k - 1]) * fs[k]
                if sum == float(constraint[-1]):
                    temp = 1
                    for i in constraint[:-2]:
                        if i != 0 and not temp in fs:
                            final_solution[temp] = 0.0
                        temp += 1

        # merging solutions dictionaries
        fs = fs | final_solution

        for i in range(1, orig_variables + 1):
            if i in fs:
                print("x" + str(i) + "=" + str(round(fs[i], bound)))
            else:
                print("x" + str(i) + "=" + str(0.0))

        if message == "finished":
            sum = 0
            for i in range(len(optimization)):
                if i + 1 in fs.keys():
                    sum += fs[i + 1] * float(optimization[i])
            print("for the value of: ", round(sum, bound))
