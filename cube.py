import numpy as np
import sys
import random
from stringcolor import *
import math
import helper

# 90 degree rotations in the XY plane. CW is clockwise, CC is counter-clockwise.
ROT_XY_CW = np.array([[0, 1, 0],
                      [-1, 0, 0],
                      [0, 0, 1]])
ROT_XY_CC = np.array([[0, -1, 0],
                      [1, 0, 0],
                      [0, 0, 1]])

# 90 degree rotations in the XZ plane (around the y-axis when viewed pointing toward you).
ROT_XZ_CW = np.array([[0, 0, -1],
                      [0, 1, 0],
                      [1, 0, 0]])
ROT_XZ_CC = np.array([[0, 0, 1],
                      [0, 1, 0],
                      [-1, 0, 0]])

# 90 degree rotations in the YZ plane (around the x-axis when viewed pointing toward you).
ROT_YZ_CW = np.array([[1, 0, 0],
                      [0, 0, 1],
                      [0, -1, 0]])
ROT_YZ_CC = np.array([[1, 0, 0],
                      [0, 0, -1],
                      [0, 1, 0]])

test_moves = "F B L R U D D' U' R' L' B' F' F2 B2 L2 R2 U2 D2 D2 U2 R2 L2 B2 F2"


class Cube:
    # F, B, L, R, U, D
    # 0 null, 1 red, 2 orange, 3 green, 4 blue, 5 white, 6 yellow

    # cube is stored in 3D array
    # cube stores the current cube and all its changes
    # pieces links to its piece in cube but doesnt change indexes
    cube = [[[0 for z in range(3)] for y in range(3)] for x in range(3)]
    pieces = [[[0 for z in range(3)] for y in range(3)] for x in range(3)]

    valid_moves = ["L", "U", "F", "D", "R", "B", "L'", "U'",
                   "F'", "D'", "R'", "B'", "L2", "U2", "F2", "D2", "R2", "B2"]

    # the rotation matrix for numpy for each face
    move_config = {
        "F": [[0, 1, 2], [0, 1, 2], [2], ROT_XY_CC],
        "B": [[0, 1, 2], [0, 1, 2], [0], ROT_XY_CW],
        "U": [[0, 1, 2], [2], [0, 1, 2], ROT_XZ_CC],
        "D": [[0, 1, 2], [0], [0, 1, 2], ROT_XZ_CW],
        "L": [[0], [0, 1, 2], [0, 1, 2], ROT_YZ_CW],
        "R": [[2], [0, 1, 2], [0, 1, 2], ROT_YZ_CC],

        "F'": [[0, 1, 2], [0, 1, 2], [2], ROT_XY_CW],
        "B'": [[0, 1, 2], [0, 1, 2], [0], ROT_XY_CC],
        "U'": [[0, 1, 2], [2], [0, 1, 2], ROT_XZ_CW],
        "D'": [[0, 1, 2], [0], [0, 1, 2], ROT_XZ_CC],
        "L'": [[0], [0, 1, 2], [0, 1, 2], ROT_YZ_CC],
        "R'": [[2], [0, 1, 2], [0, 1, 2], ROT_YZ_CW]
    }

    faces = {
        "F": [[0, 1, 2], [0, 1, 2], [2], 2],
        "B": [[0, 1, 2], [0, 1, 2], [0], 2],
        "U": [[0, 1, 2], [2], [0, 1, 2], 1],
        "D": [[0, 1, 2], [0], [0, 1, 2], 1],
        "L": [[0], [0, 1, 2], [0, 1, 2], 0],
        "R": [[2], [0, 1, 2], [0, 1, 2], 0],
    }
    #constructor for the cube object which stores the cubies
    # colours are stored as a 3 character list representing xyz planes
    # ie if you have [W, B, R] W is on the x axis
    # N means no colour
    # point stores the cubies position in the cube array
    def __init__(self):
        c = self.cube
        self.debug = False
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    colours = [0, 0, 0]
                    colours[0] = 'G' if x == 0 else 'B' if x == 2 else 'N'
                    colours[1] = 'Y' if y == 0 else 'W' if y == 2 else 'N'
                    colours[2] = 'O' if z == 0 else 'R' if z == 2 else 'N'

                    point = [x, y, z]
                    self.cube[x][y][z] = Cubie(colours, point)
                    self.pieces[x][y][z] = self.cube[x][y][z]

    #returns the colours on a chosen face
    def get_face(self, xrng, yrng, zrng, face):
        c = self.cube

        out = ['N' for x in range(9)]
        i = 0
        for x in xrng:
            for y in yrng:
                for z in zrng:
                    out[i] = self.cube[x][y][z].colours[face]
                    i += 1
        return out

    #dict for adding the colours to the cube display in terminal
    cols = {'B': "blue", 'R': "red", 'G': "green",
            'O': "DarkOrange", 'W': "white", 'Y': "Yellow4"}

    #tostring function which prints the cube object in a reader friendly view in the terminal
    def __str__(self):
        c = self.cube
        string = f"""
                {cs(c[0][2][0].colours[1], self.cols[c[0][2][0].colours[1]])} {cs(c[1][2][0].colours[1], self.cols[c[1][2][0].colours[1]])} {cs(c[2][2][0].colours[1], self.cols[c[2][2][0].colours[1]])}
                {cs(c[0][2][1].colours[1], self.cols[c[0][2][1].colours[1]])} {cs(c[1][2][1].colours[1], self.cols[c[1][2][1].colours[1]])} {cs(c[2][2][1].colours[1], self.cols[c[2][2][1].colours[1]])}
                {cs(c[0][2][2].colours[1], self.cols[c[0][2][2].colours[1]])} {cs(c[1][2][2].colours[1], self.cols[c[1][2][2].colours[1]])} {cs(c[2][2][2].colours[1], self.cols[c[2][2][2].colours[1]])}
        {cs(c[0][2][0].colours[0], self.cols[c[0][2][0].colours[0]])} {cs(c[0][2][1].colours[0], self.cols[c[0][2][1].colours[0]])} {cs(c[0][2][2].colours[0], self.cols[c[0][2][2].colours[0]])}   {cs(c[0][2][2].colours[2], self.cols[c[0][2][2].colours[2]])} {cs(c[1][2][2].colours[2], self.cols[c[1][2][2].colours[2]])} {cs(c[2][2][2].colours[2], self.cols[c[2][2][2].colours[2]])}   {cs(c[2][2][2].colours[0], self.cols[c[2][2][2].colours[0]])} {cs(c[2][2][1].colours[0], self.cols[c[2][2][1].colours[0]])} {cs(c[2][2][0].colours[0], self.cols[c[2][2][0].colours[0]])}   {cs(c[2][2][0].colours[2], self.cols[c[2][2][0].colours[2]])} {cs(c[1][2][0].colours[2], self.cols[c[1][2][0].colours[2]])} {cs(c[0][2][0].colours[2], self.cols[c[0][2][0].colours[2]])}
        {cs(c[0][1][0].colours[0], self.cols[c[0][1][0].colours[0]])} {cs(c[0][1][1].colours[0], self.cols[c[0][1][1].colours[0]])} {cs(c[0][1][2].colours[0], self.cols[c[0][1][2].colours[0]])}   {cs(c[0][1][2].colours[2], self.cols[c[0][1][2].colours[2]])} {cs(c[1][1][2].colours[2], self.cols[c[1][1][2].colours[2]])} {cs(c[2][1][2].colours[2], self.cols[c[2][1][2].colours[2]])}   {cs(c[2][1][2].colours[0], self.cols[c[2][1][2].colours[0]])} {cs(c[2][1][1].colours[0], self.cols[c[2][1][1].colours[0]])} {cs(c[2][1][0].colours[0], self.cols[c[2][1][0].colours[0]])}   {cs(c[2][1][0].colours[2], self.cols[c[2][1][0].colours[2]])} {cs(c[1][1][0].colours[2], self.cols[c[1][1][0].colours[2]])} {cs(c[0][1][0].colours[2], self.cols[c[0][1][0].colours[2]])}
        {cs(c[0][0][0].colours[0], self.cols[c[0][0][0].colours[0]])} {cs(c[0][0][1].colours[0], self.cols[c[0][0][1].colours[0]])} {cs(c[0][0][2].colours[0], self.cols[c[0][0][2].colours[0]])}   {cs(c[0][0][2].colours[2], self.cols[c[0][0][2].colours[2]])} {cs(c[1][0][2].colours[2], self.cols[c[1][0][2].colours[2]])} {cs(c[2][0][2].colours[2], self.cols[c[2][0][2].colours[2]])}   {cs(c[2][0][2].colours[0], self.cols[c[2][0][2].colours[0]])} {cs(c[2][0][1].colours[0], self.cols[c[2][0][1].colours[0]])} {cs(c[2][0][0].colours[0], self.cols[c[2][0][0].colours[0]])}   {cs(c[2][0][0].colours[2], self.cols[c[2][0][0].colours[2]])} {cs(c[1][0][0].colours[2], self.cols[c[1][0][0].colours[2]])} {cs(c[0][0][0].colours[2], self.cols[c[0][0][0].colours[2]])}
                {cs(c[0][0][2].colours[1], self.cols[c[0][0][2].colours[1]])} {cs(c[1][0][2].colours[1], self.cols[c[1][0][2].colours[1]])} {cs(c[2][0][2].colours[1], self.cols[c[2][0][2].colours[1]])}
                {cs(c[0][0][1].colours[1], self.cols[c[0][0][1].colours[1]])} {cs(c[1][0][1].colours[1], self.cols[c[1][0][1].colours[1]])} {cs(c[2][0][1].colours[1], self.cols[c[2][0][1].colours[1]])}
                {cs(c[0][0][0].colours[1], self.cols[c[0][0][0].colours[1]])} {cs(c[1][0][0].colours[1], self.cols[c[1][0][0].colours[1]])} {cs(c[2][0][0].colours[1], self.cols[c[2][0][0].colours[1]])}"""
        return string

    #returns the colours from lists of xyz (selects only the colours that need to move as the face rotates)
    def get_colour_indexs(self, lists):
        colours = []
        for i in range(3):
            if len(lists[i]) > 1:
                colours.append(i)
        return colours

    #rotates a face on the cube using x,y,z ranges and a rotation matrix to calculate new positions
    def rot_face(self, move_conf):
        c = self.cube
        xrng, yrng, zrng, rot_matrix = move_conf
        c_i = self.get_colour_indexs([xrng, yrng, zrng])

        # the indexes change from 0 to 2 to -1 to 1 for the transformation
        trans = [[[0 for z in range(3)] for y in range(3)] for x in range(3)]
        for x in xrng:
            for y in yrng:
                for z in zrng:
                    matrix = np.dot([x - 1, y - 1, z - 1], rot_matrix)
                    matrix = [matrix[0] + 1, matrix[1] + 1, matrix[2] + 1]
                    trans[matrix[0]][matrix[1]][matrix[2]] = c[x][y][z]

                    tc = trans[matrix[0]][matrix[1]][matrix[2]].colours
                    tc[c_i[0]], tc[c_i[1]] = tc[c_i[1]], tc[c_i[0]]

                    trans[matrix[0]][matrix[1]][matrix[2]].point = [
                        matrix[0], matrix[1], matrix[2]]

        for x in xrng:
            for y in yrng:
                for z in zrng:
                    c[x][y][z] = trans[x][y][z]

    #takes in a move and executes it using the rot_face function
    def exe_move(self, move):
        if "2" in move:
            move = move[:1]
            self.rot_face(self.move_config[move])
        self.rot_face(self.move_config[move])

    #applies list of moves and calls function to execute them
    def do_moves(self, moves):
        for move in moves:
            self.exe_move(move)

    # takes in a number x and randomly chooses x moves to apply to the cube to scramble it
    def scramble(self, moves):
        moves_list = []
        for i in range(moves):
            new_move = random.choice(self.valid_moves)
            if len(moves_list):
                while new_move[0] in moves_list[-1]:
                    new_move = random.choice(self.valid_moves)
            moves_list.append(new_move)
            self.exe_move(new_move)
        return moves_list

    #checks if the cube is solved using the colours on a face
    def is_solved(self):
        faces = ["F", "B", "U", "D", "L", "R"]
        colours = []
        for face in faces:
            x, y, z, f = self.faces[face]
            colours = (self.get_face(x, y, z, f))
            if helper.check_face(colours) == False:
                return False
        return True

#class of the 26 cubies in the 3x3 cube
class Cubie:
    # x face y face z face colours
    colours = ['N' for x in range(3)]

    #constructor to create a cubie with colours and xyz location
    def __init__(self, colours, point):
        self.colours = colours
        self.point = point
