"""
NAME    helpers.py

AUTHOR  Jos Feenstra
        Tara Elsen
        Christiaan Wewer

DATE    18-12-2017 (last edit)

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
from math import sqrt, pi

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
VALUE          = [285000,    399000,     610000     ]
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
