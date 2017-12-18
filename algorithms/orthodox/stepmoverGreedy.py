"""
NAME:        stepmoverGreedy.py
AUTHORS:     Jos Feenstra & Tara Elsen
PURPOSE:     This algorithm finds a map's local optimum by suddle house movement
NOTES:       This algorithm works great as a "cherry on top" algorithm.
             It isnt capable of doing amazing optimalization, but it will
             improve maps created by other algorithms with greater precision than other greedy algorithms

DESCRIPTION: Load a map
             repeat the following process until the map doesnt improve anymore:
                per houses of map:
                    find a houses' best location by:
                    move of size STEP in 8 winddirections: [N, NE, E, ZE, Z, ZW, W, NW]
                    if the map value improves by this move:
                        keep the move.
                    if all moves cannot be done:
                        decrease STEP size
                        if step is 0.5
                            return , house has found its local optimum, move on to next house, and repeat process
"""

import sys
sys.path.append("..")
from dependencies.helpers import *

fileName = "upperboundstatespace20"
dirPath = "C:\\Users\\Jos\\GitHub\\AmstelHaegeNew\\Saves\\json"

def main():

    # get arguments
    houseTypes = initHouseTypes(100)

    # make fill and plot the map
    map1 = Map()
    map1.loadJSON(dirPath, fileName, houseTypes, False)

    # show beforehands
    map1.addWater()
    map1.plot()
    map1.waterBody.clear()

    cherryImprove(map1)

    # show result
    map1.addWater()
    map1.plot()
    map1.waterBody.clear()

def cherryImprove(aMap):
    """
    keeps improving the house locations of 'aMap', until they cant be improved anymore
    (using this algorithm atleast)
    """

    # use certain data to create vectors
    # increments = [128, 64, 32, 16, 8, 4, 2, 1, 0.5]
    increments = [16, 8, 4, 2, 1, 0.5]

    # keep looping until the map value wont improve anymore
    originalValue = aMap.calculateValue()

    reverse = aMap.house
    while(True):
        print("opnieuw")
        for house in reverse:
            # move 1 house to its move valuable position
            others = [h.boundary for h in aMap.house if h is not house]
            moveToIdealPosition(house, aMap, increments, others)

        # break if the map value is not improving anymore
        newValue = aMap.calculateValue()

        highscore = 19000000
        # print at a certain point
        if printAt(aMap, newValue, highscore):
            highscore = newValue

        if originalValue < newValue:
            # map has improved, redo proccess
            originalValue = newValue
        elif originalValue == newValue:
            # map has not improved
            print("peak reached, we need more sim annealing!!")
            break
        else:
            print("the cherry algorithm is doing weird things... new value is lower for some reason")
            break

def moveToIdealPosition(house, aMap, increments, otherBoundaries):
    """
    moves a house to a position that will have the best map value possible
    """
    # starting value
    start = aMap.calculateValue()

    # per increment
    for inc in increments:

        # per direction option with that increment
        up    = (0,  inc)
        down  = (0, -inc)
        left  = (-inc, 0)
        right = ( inc, 0)
        upleft    = moveCoord(up,   left)
        upright   = moveCoord(up,   right)
        downleft  = moveCoord(down, left)
        downright = moveCoord(down, right)
        direction = [up, down, left, right, upleft, upright, downleft, downright]
        dir_length = len(direction)

        # loop though all directions
        for i in range(dir_length):

            # repeat until unvalid
            while(True):
                origin = house.origin
                house.move(direction[i])
                change = aMap.calculateValue()

                if (change > start and
                    house.isWithinMap() and
                    not house.boundary.isTouchingTight(otherBoundaries)):
                    # take the move
                    print(inc)
                    start = change
                else:
                    # reject move
                    house.relocate(origin)
                    break

def printAt(aMap, mapVal, value):
    if mapVal > value:
        aMap.plot()
        aMap.saveJSON(dirPath, "{}_cherrymover".format(mapVal))
        return True
    return False

if __name__ == "__main__":
    main()
