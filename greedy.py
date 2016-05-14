#!/usr/env/python3

from math import sqrt

# Evaluating average distance (between aspirants and locations)
# type :: ( [[float]], [int] ) -> float
def averageDistance(M, assignment):
    return sum([ M[i][ assignment[i] ] for i in range(len(assignment)) ]) / len(assignment)

# Defining distance between two points in space
# type :: (float, float) -> float
def d(a, b):
    x1, y1 = a
    x2, y2 = b
    return sqrt( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )

# given a matrix with the distances and the capacity of the locations return
# an assignment (using a greedy algorithm)
# type :: ( [[float]], [int] ) -> [int]
def greedyAssignment(M, cs):
    n_locs = len(cs)
    n_ants = len(M)
    cpcties = cs[:] # copying capacities

    snd = lambda xs: xs[1] # second field of a tuple (actually, anything that has the __getitem__ attibute

    # aspirants sorted by their closeness to their closest presentation location
    # type :: [ (int, [ (int, float) ]) ]
    closestLoc = sorted(
                    [
                    (i, sorted( [(j, M[i][j]) for j in range(n_locs)] , key=snd))
                    for i in range(len(M))
                    ]
                    , key=lambda a: snd(a[1]) )

    # creating assingment list
    # type :: [int]
    assignment = [-1 for i in range(n_ants)]

    # assigning locations to each aspirant, first those who live the closest
    # to their closest presentantion locations
    for aspirant, locations in closestLoc:
        for l,_ in locations:
            if cpcties[l] > 0:
                assignment[aspirant] = l
                cpcties[l] -= 1
                break

    return assignment

# Random assignment respecting capacities
# type :: ( [[float]], [int] ) -> [int]
def randomAssignment(M, cs):
    from random import randint

    n_locs = len(cs)
    n_ants = len(M)
    cpcties = cs[:] # copying capacities

    assignment = [-1 for i in range(n_ants)]

    for aspirant in range(n_ants):
        # getting random location with capacity
        loc = randint(0, n_locs-1)
        while cpcties[loc] == 0:
            loc = randint(0, n_locs-1)

        # assigning location
        assignment[aspirant] = loc
        cpcties[loc] -= 1

    return assignment

# Testing the code
# type :: string -> None
def main(input_lines = None):
    if len(input_lines) == None:
        from random import randint, random

        n_locs = 30   # number of locations
        n_ants = 40000  # number of aspirants

        # Creating random capacities
        cpcties = [randint(20, 1700) for i in range(n_locs)]
        while sum(cpcties) < n_ants:
            cpcties = [c+10 for c in cpcties]

        # Creating random (x,y) coordinates for Locations and aspirants
        locations = [(random(), random()) for i in range(n_locs)]
        aspirants = [(random(), random()) for i in range(n_ants)]

        # saving random test
        #f = open('large_example.csv', 'w')
        #f.write( "{:d};{:d}\n".format(n_locs, n_ants) )
        #
        #for i in range(n_locs):
        #    x, y = locations[i]
        #    f.write( "{:02d};{:d};{:f};{:f}\n".format(i, cpcties[i], x, y))
        #
        #for i in range(n_ants):
        #    x, y = aspirants[i]
        #    f.write( "{:05d};{:f};{:f}\n".format(i, x, y))
        #
        #f.close()

    else:
        n_locs, n_ants = input_lines[0].split(";")
        n_locs, n_ants = int(n_locs), int(n_ants)

        cpcties = [ int(loc.split(";")[1]) for loc in input_lines[1:n_locs+1] ]

        # line to coordinates
        # type :: [string] -> (float, float)
        toCoord = lambda l: (float(l[0]), float(l[1]))

        locations = [ toCoord(loc.split(";")[2:]) for loc in input_lines[1:n_locs+1] ]
        aspirants = [ toCoord(asp.split(";")[1:]) for asp in input_lines[n_locs+1:] ]

    # Creating matrix with distances from aspirants to locations
    M = [ [d(locations[l], a) for l in range(n_locs)]
            for a in map(lambda i: aspirants[i], range(n_ants))
        ]

    assignment = greedyAssignment(M, cpcties)
    assignment2 = randomAssignment(M, cpcties)

    distance = averageDistance(M, assignment)
    distance2 = averageDistance(M, assignment2)

    print( "Capacities:", cpcties )
    print( " == Mean distance == ")
    print( "Assignment (greedy): {:f}".format(distance) )
    print( "Assignment (random): {:f}".format(distance2) )


def mode_of_use():
    print("Mode of use: python3 {:s} [-i|--input inputfile.txt]\n".format( argv[0] ) )
    print("  Input file format: \n"+
          "  line | content                                          \n"+
          " ----- | -------------------------------------------------\n"+
          "     1 | number_of_locations; number_of_aspirants         \n"+
          "   n+1 | location_n_capacity; location_n_x_coord; y_coord \n"+
          "       | ...                                              \n"+
          " n+m+1 | aspirant_m_id; aspirant_m_x_coord; y_coord")
    exit(1)

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 1:
        main()
    elif len(argv) == 3 and argv[1] in ['-i', '--input']:
        main( open(argv[2], 'r').readlines() )
    else:
        mode_of_use()
