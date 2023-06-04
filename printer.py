def print_simplex(simplex_tableau):
    for i in range(simplex_tableau[0].__len__()):
        for j in range(simplex_tableau.__len__()):
            print("{:.5f}".format(simplex_tableau[j][i]), end=" " * 6)
        print("")
    print("\n")
