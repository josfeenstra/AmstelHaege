
from dependencies.helpers import *

fileName = "33127104_cherrymover"
dirPath = "C:\\Users\\Jos\\GitHub\\UrbanPlanning\\Rhino\\json"

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

def calcTemperaturBasedOn(disprovement, housetype, inc):
    """
    disprovement ranges from -? to 0
    """
    dispr = abs(disprovement)
    if housetype == 2:

        # return 0 underneath lowerBound
        lowerBound = 1 * inc
        # return maxchance above upperbound
        upperBound = 0
        maxChance = 0.8

    elif housetype == 1:

        # return 0 underneath lowerBound
        lowerBound = 200000 * inc
        # return maxchance above upperbound
        upperBound = 0
        maxChance = 0.3

    else:

        # return 0 underneath lowerBound
        lowerBound = 200000 * inc
        # return maxchance above upperbound
        upperBound = 0
        maxChance = 0.2

    # linear
    temperature = (lowerBound - dispr) / lowerBound * maxChance
    # print(temperature)
    return temperature

def simAnnealing(temperature):
    # calc values to compare
    random0to1 = random()

    # perform check
    if temperature >= random0to1:
        return True
    else:
        return False

def cherryImproveSA(aMap):
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
    simanneal = False
    while(True):
        print("opnieuw")
        for house in reverse:
            # move 1 house to its move valuable position
            others = [h.boundary for h in aMap.house if h is not house]
            if simanneal:
                print("sim")
                moveToIdealPositionSA(house, aMap, increments, others)
            else:
                print("greedy")
                moveToIdealPosition(house, aMap, increments, others)

        if simanneal:
            simanneal = False
        else:
            simanneal = True

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
            # break
        else:
            print("the cherry algorithm is doing weird things... new value is lower for some reason")
            # break

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

def moveToIdealPositionSA(house, aMap, increments, otherBoundaries):
    """
    moves a house to a position that will have the best map value possible
    """
    # starting value
    start = aMap.calculateValue()

    # number of iterations since a correct move


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

                # calcutate temperature for simAnnealing
                temp = 0

                # calculate how much the map has improved
                mapimprovement = change - start

                # check if the move is valid
                if (house.isWithinMap() and
                    not house.boundary.isTouchingTight(otherBoundaries) and
                    change is not -1):
                    # check if the move improves the map
                    if mapimprovement > 0:
                        temp = 1
                    else:
                        temp = calcTemperaturBasedOn(mapimprovement, house.type.integer, inc) # number of unchanged houses up to this point
                else:
                    # move is not allowed (could be changed for constraints relaxation)
                    temp = 0

                # now let simannealing deside to accept the move or not
                if simAnnealing(temp):
                    # accept move
                    print(inc)
                    start = change
                else:
                    # do not accept move
                    house.relocate(origin)
                    break

def printAt(aMap, mapVal, value):
    if mapVal > value:
        aMap.plot()
        aMap.saveJSON(dirPath, "{}_cherrymover".format(mapVal))
        return True
    return False

# # make a swapper
# def swapGreedy(aMap):
#     # CALCULATE vALUE NEEDS TO BE USED ONCE BEFORE!!
#     data = []
#     for house in aMap.house:
#         pair = (house.shortest, house.type.integer)
#
#         # add data to list
#         data.append(pair)
#
#     # sort the list
#     data = sorted(data, key=operator.itemgetter(0))
#
#     print(data)
#
#     # find family home with the most value
#     bungalowdata = [d for d in data if d[1] is 1]
#     familydata = [d for d in data if d[1] is 0]
#     print(max(familydata, key=operator.itemgetter(0)))
#     print(min(bungalowdata, key=operator.itemgetter(0)))
#     # find bungalow with the smallest value
#
#     # if the biggest shortest of family home is bigger than the smallest bungalow:
#         # swap them
#
#     def swapHouses(house1, house2):
#         loc1 = house1.origin
#         loc2 = house2.origin
#         house1.relocate(loc1)
#         house2.relocate(loc2)
#
# def main2():
#
#     # get arguments
#     houseTypes = initHouseTypes(100)
#
#     # make fill and plot the map
#     map1 = Map()
#     map1.loadJSON(dirPath, fileName, houseTypes, False)
#     map1.plot()
#     map1.calculateValue()
#     swapGreedy(map1)

if __name__ == "__main__":
    main()
