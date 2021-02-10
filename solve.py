import helper
import cube
from cube import np

Right = {
    "D": "D",
    "U": "U",
    "D'": "D'",
    "U'": "U'",
    "D2": "D2",
    "U2": "U2",
    "R": "B",
    "L": "F",
    "F": "R",
    "B": "L",
    "R'": "B'",
    "L'": "F'",
    "F'": "R'",
    "B'": "L'",
    "R2": "B2",
    "L2": "F2",
    "F2": "R2",
    "B2": "L2",
}

Left = {
    "D": "D",
    "U": "U",
    "D'": "D'",
    "U'": "U'",
    "D2": "D2",
    "U2": "U2",
    "L": "B",
    "R": "F",
    "F": "L",
    "B": "R",
    "L'": "B'",
    "R'": "F'",
    "F'": "L'",
    "B'": "R'",
    "L2": "B2",
    "R2": "F2",
    "F2": "L2",
    "B2": "R2",
}

Back = {
    "D": "D",
    "U": "U",
    "D'": "D'",
    "U'": "U'",
    "D2": "D2",
    "U2": "U2",
    "R": "L",
    "L": "R",
    "F": "B",
    "B": "F",
    "R'": "L'",
    "L'": "R'",
    "F'": "B'",
    "B'": "F'",
    "R2": "L2",
    "L2": "R2",
    "F2": "B2",
    "B2": "F2",
}


class Algos:
    # get the side of the correlated coords [x, z]
    coord_to_side = {
        (1, 0): "B",
        (0, 1): "L",
        (2, 1): "R",
        (1, 2): "F"
    }

    # colour to cooord: tuple of x and z of the face
    c_t_c = {
        "O": (1, 0),
        "G": (0, 1),
        "B": (2, 1),
        "R": (1, 2)
    }

    side_to_coord = {
        "B": (1, 0),
        "L": (0, 1),
        "R": (2, 1),
        "F": (1, 2)
    }

    side_colour = {
        "F": "R",
        "B": "O",
        "L": "G",
        "R": "B",
        "U": "W",
        "D": "Y"
    }

    # colour to side
    c_t_s = {
        "R": "F",
        "O": "B",
        "G": "L",
        "B": "R",
        "W": "U",
        "Y": "D"
    }

    right_col_of_face = {
        (0, 0): "O",
        (0, 2): "G",
        (2, 0): "B",
        (2, 2): "R"
    }

    def __init__(self, cube):
        # self.cube = c
        self.cube = cube
        self.c = cube.cube
        self.moves = []
        self.debug = cube.debug

    def get_center_colour(self, cubie):
        return [x for x in cubie.colours if x not in "N"][0]

    def write_exe_moves(self, moves):
        self.moves.extend(moves)
        self.cube.do_moves(moves)
        if self.debug == True:
            print(*moves)
            print(self.cube)

    def cross(self):
        c = self.c

        for colour in ["R", "B", "O", "G"]:
            cubie = self.cube.find_cubie([colour, "W", "N"])

            # if cubie is on the white face
            if (cubie.point[1] == 2):
                # if (cubie.colours[1] == "W") and (self.cube.cube[x][2][z] is cubie):
                #         continue
                self.write_exe_moves(
                    [self.coord_to_side[(cubie.point[0], cubie.point[2])] + "2"])
            # if cubie is in the middle
            if (cubie.point[1] == 1):
                # this is borked need to find which face it is on
                self.write_exe_moves(move_translator(
                    self.right_col_of_face[(cubie.point[0], cubie.point[2])], ["F", "D", "F'"]))
            # change to use point
            center = self.c[(self.c_t_c[colour])[0]
                            ][1][(self.c_t_c[colour])[1]]
            # change to use point
            while not self.c[self.c_t_c[colour][0]][0][self.c_t_c[colour][1]] == cubie:
                self.write_exe_moves(["D"])
            if cubie.colours[1] == "W":
                self.write_exe_moves([move_translator(colour, "F")[0] + "2"])
            else:
                self.write_exe_moves(move_translator(
                    colour, "F' U' R U".split()))

    def white_corner_helper(self, xy, moves):
        self.write_exe_moves(move_translator(
            self.right_col_of_face[xy], moves))

    def white_corners(self):
        for x in [0, 2]:
            for z in [0, 2]:
                cubie = self.cube.pieces[x][2][z]

                if cubie.point[1] == 2:
                    if (cubie.colours[1] == "W") and (self.cube.cube[x][2][z] is cubie):
                        continue
                    self.white_corner_helper(
                        (cubie.point[0], cubie.point[2]), ["R'", "D'", "R"])

                while not ((cubie.point[0] == x) and (cubie.point[2] == z)):
                    self.write_exe_moves(['D'])

                if cubie.colours[1] == "W":
                    self.white_corner_helper((x, z), ["R'", "D", "R", "D2"])

                if (cubie.colours[2] == "W" and x == z) or (cubie.colours[0] == "W" and x != z):
                    self.white_corner_helper((x, z), ["F", "D", "F'"])
                else:
                    self.white_corner_helper((x, z), ["R'", "D'", "R"])

    def middle_edges(self):
        ROT_XZ_CW = np.array([[0, 0, -1],
                              [0, 1, 0],
                              [1, 0, 0]])

        for x in [0, 2]:
            for z in [0, 2]:
                cubie = self.cube.pieces[x][1][z]

                if cubie.point[1] == 1:
                    # idk if this works
                    # if (self.c[x][2][z] is cubie) and (cubie.point[0] == self.c[1][1][z]):
                    #     continue
                    self.white_corner_helper(
                        (cubie.point[0], cubie.point[2]), ["R'", "D", "R", "D", "F", "D'", "F'"])

                # cubie colour
                cc = cubie.colours[2 if cubie.point[0] == 1 else 0]
                while cc != self.c[cubie.point[0]][1][cubie.point[2]].colours[2 if cubie.point[0] == 1 else 0]:
                    self.write_exe_moves(['D'])
                    cc = cubie.colours[2 if cubie.point[0] == 1 else 0]

                # right center
                rc = np.dot(
                    [cubie.point[0] - 1, 0, cubie.point[2] - 1], ROT_XZ_CW)
                if cubie.colours[1] == self.c[rc[0] + 1][1][rc[2] + 1].colours[0 if cubie.point[0] == 1 else 2]:
                    self.write_exe_moves(move_translator(
                        cc, ["D'", "R'", "D", "R", "D", "F", "D'", "F'"]))
                else:
                    self.write_exe_moves(move_translator(
                        cc, ["D", "L", "D'", "L'", "D'", "F'", "D", "F"]))

    def yellow_cross(self):
        if not (self.c[1][0][0].colours[1] == "Y" and self.c[1][0][2].colours[1] == "Y" and self.c[0][0][1].colours[1] == "Y" and self.c[2][0][1].colours[1] == "Y"):
            if not (self.c[1][0][0].colours[1] == self.c[1][0][2].colours[1] or self.c[0][0][1].colours[1] == self.c[2][0][1].colours[1]):
                if self.c[1][0][0].colours[1] == "Y" or self.c[1][0][2].colours[1] == "Y":
                    while not (self.c[1][0][0].colours[1] == "Y" and self.c[2][0][1].colours[1] == "Y"):
                        self.write_exe_moves(["D"])
                self.write_exe_moves(
                    ["F", "L", "D", "L'", "D'", "L", "D", "L'", "D'", "F'", "D"])
            elif self.c[1][0][2].colours[1] == "Y":
                self.write_exe_moves(["D"])

            if self.c[1][0][2].colours[1] != "Y":
                self.write_exe_moves(["F", "L", "D", "L'", "D'", "F'"])

    def yellow_edges(self):
        opposite_colour = {
            "O": "R",
            "R": "O",
            "B": "G",
            "G": "B"
        }
        adj_colour = {
            "O": "B",
            "R": "G",
            "B": "R",
            "G": "O"
        }

        if not (opposite_colour[self.c[1][0][0].colours[2]] == self.c[1][0][2].colours[2] and adj_colour[self.c[1][0][2].colours[2]] == self.c[1][0][2].colours[2]):
            if (opposite_colour[self.c[1][0][0].colours[2]] == self.c[1][0][2].colours[2] or opposite_colour[self.c[0][0][1].colours[0]] == self.c[2][0][1].colours[0]):
                if opposite_colour[self.c[0][0][1].colours[0]] == self.c[2][0][1].colours[0]:
                    self.write_exe_moves(["D"])
                self.write_exe_moves(
                    ["L", "D", "L'", "D", "L", "D", "D", "L'"])

            while adj_colour[self.c[0][0][1].colours[0]] != self.c[1][0][0].colours[2]:
                self.write_exe_moves(["D"])
            self.write_exe_moves(["L", "D", "L'", "D", "L", "D", "D", "L'"])

            while self.c[1][1][2].colours[2] != self.c[1][0][2].colours[2]:
                self.write_exe_moves(["D"])

    def check_yellow_corners(self):
        yes_cubies = []
        for x in [0, 2]:
            for z in [0, 2]:
                if self.get_center_colour(self.c[x][1][1]) in self.c[x][0][z].colours and self.get_center_colour(self.c[1][1][z]) in self.c[x][0][z].colours:
                    yes_cubies.append((x, z))

        return yes_cubies

    lor_face_of_col = {
        (0, 0, "l"): "O",
        (0, 0, "r"): "G",
        (0, 2, "l"): "G",
        (0, 2, "r"): "R",
        (2, 0, "l"): "B",
        (2, 0, "r"): "O",
        (2, 2, "l"): "R",
        (2, 2, "r"): "B"
    }

    def yellow_corner_setup(self):

        correct_cubies = self.check_yellow_corners()

        while len(correct_cubies) != 4:
            self.write_exe_moves(move_translator(self.lor_face_of_col[correct_cubies[0][0], correct_cubies[0][1], "l"] if len(
                correct_cubies) == 1 else "F", ["D'", "R'", "D", "L", "D'", "R", "D", "L'"]))
            correct_cubies = self.check_yellow_corners()

    def yellow_corner_rot(self):
        for i in range(4):
            while self.c[2][0][2].colours[1] != "Y":
                self.write_exe_moves(["R", "U", "R'", "U'"])
            self.write_exe_moves(["D"])


# up and down not included here


def move_translator(face, moves):
    new_moves = []
    for move in moves:
        if face == "R":
            new_moves.append(move)
        elif face == "G":
            move = Left[move]
            new_moves.append(move)
        elif face == "B":
            move = Right[move]
            new_moves.append(move)
        elif face == "O":
            move = Back[move]
            new_moves.append(move)
        else:
            new_moves.append(move)
    return(new_moves)

# print(move_translator("L", "R'"))


def solve(cube):
    if cube.is_solved():
        print("cube already solved, no solution needed")
        exit()

    algos = Algos(cube)

    algos.cross()
    algos.white_corners()
    algos.middle_edges()
    algos.yellow_cross()
    algos.yellow_edges()
    algos.yellow_corner_setup()
    algos.yellow_corner_rot()

    algos.moves = helper.optimise_all(algos.moves)
    
