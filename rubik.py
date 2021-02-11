import sys
import helper
import cube
import solve

def main():
    args = sys.argv
    debug = False
    pretty_print = False
    i = 0
    #check for -v (debug) -p (pretty print) or too many args
    if len(args) == 3:
        while i < len(args):
            if args[i] == "-v":
                debug = True
                if pretty_print == True:
                    print("invalid number or type of arguments")
                    return False
                del args[i]
                i = 0
            i += 1
    if len(args) != 2:
        print("invalid number and type of arguments")
        return False

    #allow user to choose how long the scramble is
    if sys.argv[1] == "-r":
        number = input("How many moves would you like to scramble? ")
        while not helper.is_int(number):
            print("please provide a positive integer number for how many moves you want generated")
            number = input("How many moves would you like to scramble? ")
        demo_cube = cube.Cube()
        print("Starting Cube:", demo_cube)
        run_cube(demo_cube, demo_cube.scramble(int(number)), 1, debug)

    #default random 20 move scramble
    elif sys.argv[1] == "-d":
        demo_cube = cube.Cube()
        print("Starting Cube:", demo_cube)
        run_cube(demo_cube, demo_cube.scramble(20), 1, debug)

    #runs the scramble 100 times with given amount of moves
    elif sys.argv[1] == "-avg":
        number = input("How many moves would you like to scramble? ")
        while not helper.is_int(number):
            print("please provide a positive integer number for how many moves you want generated")
            number = input("How many moves would you like to scramble? ")
        average_100(number, debug)

    #take user input for how to scramble the cube
    else:
        instructions = sys.argv[1]
        split_instructions = instructions.split()
        for instruction in split_instructions:
            if len(instruction) not in (1, 2):
                print ("{} is not a correct instruction (length in correct), please try again".format(instruction))
                exit()
            if instruction[0] not in ('F', 'B', 'R', 'L', 'U', 'D'):
                print ("{} is not a correct instruction (first character incorrect), please try again".format(instruction))
                exit()
            if len(instruction) == 2:
                if instruction[1] not in ('2', '\''):
                    print ("{} is not a correct instruction (second character incorrect), please try again".format(instruction))
                    exit()
        demo_cube = cube.Cube()
        print("Starting Cube:", demo_cube)
        run_cube(demo_cube, split_instructions, 0, debug)

#starts the scramble and initiates the solve and optimsation process and prints the cube
def run_cube(cube, moves, scramble, debug):
    if debug:
        cube.debug = True
    if scramble:
        print("Moves used to scramble cube : ", *moves)
        # moves = ",".join(moves)
        # print("Moves used to scramble cube : ", moves)
    else:
        cube.do_moves(moves)
        print("Moves used to scramble cube : ", *moves)
        # moves = ",".join(moves)
        # print("Moves used to scramble cube : ", moves)
    print(cube)
    sln_moves = solve.solve(cube)
    print("Solved Cube:", cube)
    if len(sln_moves) == 0:
        print("Cube already solved, no moves used.")
    else:
        print("Number of moves taken: {}".format(len(sln_moves)))
        print("Solution:", *sln_moves)
        # sln_moves = ",".join(sln_moves)
        # print("Solution:", sln_moves)

#function to run a bunch of random scrambles of specified length of moves 
# 100 times and find the average amount of moves taken to solve
def average_100(number, debug):
    i = 0
    moves_no = []
    sln_moves = []
    demo_cube = cube.Cube()
    if debug:
        cube.debug = True
    while i < 10:
        demo_cube.scramble(int(number))
        sln_moves = solve.solve(demo_cube)
        moves_no.append(len(sln_moves))
        i += 1 
    i = 0 
    total = 0
    while i < 10:
        total += moves_no[i]
        i += 1
    print("average number of moves used over 100 runs is: {}".format(total/10))

main()