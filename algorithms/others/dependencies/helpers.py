"""
NAME    helpers.py

AUTHOR  Jos Feenstra
        Tara Elsen
        Christiaan Wewer

DESC    contains all constant data, dependencies, functions and links to classes

NOTE    the minimum distance to another home is represented by the name "ring",
        as its boundary representations look like rings.

"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle as mathplot_rectangle
from matplotlib.patches import FancyBboxPatch

import numpy as np
import operator
import json
import os

from copy import copy
from random import randint, shuffle, random, randrange, choice, uniform
from collections import Iterable
from math import sqrt

# determine if algorithms should use the orthodox or unortodox approach
ORTHODOX = True

# map constances
AREA = (160, 180)
HOUSE_COUNT = [20, 40, 60]

# water constances
WATER_PERCENTAGE  = 0.20         # percentage of total area covered by water
MAX_BODIES        = 4            # maximum number of bodies
RATIO_UPPER_BOUND = 4            # l/b < x AND  b/l < x
RATIO_LOWER_BOUND = 1 / RATIO_UPPER_BOUND
WATER_COLOUR      = "b"
STARTING_WATER_ITERATION_SIZE = 1.00

# house constances
NAME           = ["Family",  "Bungalow", "Mansion"  ]
FREQUENCY      = [0.60,      0.25,       0.15       ]
    VALUE      = [285000,    399000,     610000     ]
SITE           = [(8, 8),    (10, 7.5),  (11, 10.5 )]
BASE_RING      = [2,         3,          6,         ]
RING_INCREMENT = [0.03,      0.04,       0.06       ]
COLOUR         = ["r",       'g',        'y'        ]
INTEGER        = [0,         1,          2          ]

# An unelegant element of the code
A_VERY_HIGH_INT = 50000
NONE = 50000



def initHouseTypes(IterationMax=20):
    """
    instantiate the 3 housetype objects
    """

    # determines how many rings will be added and calculated
    maximumRingIterations = IterationMax

    # make a list of House objects
    houseTypeList = list()
    for i,s in enumerate(NAME):
        houseTypeList.append(
            HouseType(NAME[i], FREQUENCY[i], VALUE[i], SITE[i], BASE_RING[i],
                RING_INCREMENT[i], maximumRingIterations, COLOUR[i], INTEGER[i])
        )
    return houseTypeList

def moveCoord(coordinate, vector):
    """
    add a coordinate and a vector (movement representative) together
    """
    return tuple(sum(x) for x in zip(coordinate, vector))
    # pick a random coord w

def randomCoord(lowestCoord, highestCoord):
    """
    pick a random coordinate,
    """
    # pick a x value
    random_x = round(uniform(lowestCoord[0], highestCoord[0]) * 2) / 2

    # pick a y value
    random_y = round(uniform(lowestCoord[1], highestCoord[1]) * 2) / 2

    return (random_x, random_y)

# import classes
from dependencies.classes import HouseType, House, WaterBody, Rectangle, Map




















"""
################################################################################
All of this stuff is junk, but it might be useful to show previous versions of
the code
################################################################################
:
"

class Coord(tuple):

    def __new__(cls, width, height):
        return tuple.__new__(cls, (width, height)) # create tuple with 2 items

    def __init__(self, x, y):
        self.x = y # width is the first argument passed
        self.y = y # height is the next



# or WAAAAYYY easier

from collections import namedtuple

Coord = namedtuple("Coord", ('x', 'y'))

# does not allow additional stuff like
coord1.move
coord1.moveto
coord1.plot


# example
coord1 = Coord(20, 40)
print(coord1)
>>> (20, 40)
print(coord1.x)
>>> 20
print(coord1.y)
>>> 40




onze case/????////// na 2e college
we moeten depth first gaan!!!!!!!
daarom eerst 1 groot apparaat maken, dan kleinere
[9][3][2][1]
[9][][][]




        # make clearer var names
        x = h.origin[0]
        y = h.origin[1]

        # push the house within bounds if the house is outside of bounds
        if x <  h.xLower:
            x = h.xLower
        if y <  h.yLower:
            y = h.yLower
        if x >= h.xUppers:
            x = h.xUpper
        if y >= h.yUpper:
            y = h.yUpper




















    # # example move
    # someVector = (100, 100)
    # someHouse.move(someVector)
    # print(someHouse.coord)


# questions about the case:
# can we turn bungalows & maisons ?
# can we
################################################################################

"
build a hardcoded map
"
def main_old1():
    ht = initHouseTypes(20)

    # example house object values
    hType = [ht[0], ht[2], ht[0], ht[1], ht[2], ht[0], ht[2], ht[0], ht[1], ht[2]]
    coordinate = [(50, 50), (64, 21), (54, 50), (84, 97), (12, 23), (45, 56), (100, 100), (30, 30), (200, 54)]
    ringsToAdd = [3, 3, 6, 4, 7, 8, 9, 3, 0, 0]

    # make a map
    map1 = Map()

    # fill the map
    for i in range(9):
        map1.addHouse(hType[i], coordinate[i], ringsToAdd[i])


    something = map1.house[1].boundary.height
    print(something)

    # draw the map
    map1.plot()



build a random map

def main_old2():
    housetypes = initHouseTypes(20)

    # generate hosue parameteres
    housetypelist = []
    for housetype in housetypes:
        n = round(housetype.frequency * SELECTED_HOUSE_COUNT)
        housetypelist += [housetype] * n

    # houstypelist = shuffle(housetypelist)

    # make a map
    map1 = Map()

    # add houses to map
    for i in range(SELECTED_HOUSE_COUNT):

        # create other parameters
        coordinate = (randint(0, AREA[0]-1), randint(0, AREA[1]-1))
        ringsToAdd = randint(1, 12)

        # add house
        map1.addHouse(housetypelist[i], coordinate, ringsToAdd)

    # draw the map
    map1.plot()




"""
