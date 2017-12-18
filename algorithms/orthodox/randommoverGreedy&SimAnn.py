"""
NAME    Random is cool

AUTHORS Christiaan Wewer & JOS FEENSTRA


DESC    MAKING THE MAP DANCE

"""

# from dependencies.helpers import *
from dependencies.helpers import *
from random import *
import matplotlib.pyplot as plt
import sys
import matplotlib.patches as mpatches
from math import e
import os
import moveStepSim

# import pandas

# choose 0, 1 or 2 to get 20, 40 or 60 houses
SELECTED_HOUSE_COUNT = 40 # HOUSE_COUNT[0]
SAVE_MAP_LOC = "C:\\Users\\chris\\Desktop\\beunSpace\\Orthodox_experimentation\\MAP_40_HOUSES"
LOAD_MAP_LOC ="C:\\Users\\chris\\Desktop\\beunSpace\\Orthodox_experimentation\\MAP_40_HOUSES"
NAME_PER_FILE = "40_house_case_"
HOW_MANY_TIMES = 5
ALG_ITERATIONS = 10000


def swapHouses(usedMap, houseIntOne, houseIntTwo):

    # swap houses
    coord1 = usedMap.house[houseIntOne].origin
    coord2 = usedMap.house[houseIntTwo].origin
    usedMap.house[houseIntOne].relocate(coord2)
    usedMap.house[houseIntTwo].relocate(coord1)


def hillclimberRandomRelocateRecursive(usedMap, startCounter, maxIterations, relocateIterations, xValues, yValues):

    # calculate mapvalue
    mapValue = usedMap.calculateValue()
    print("mapvalue before: " + str(mapValue))

    # get random house
    randHouseInt = randint(0, len(usedMap.house) - 1)

    # get coordinates from house randHouseInt
    coord1 = usedMap.house[randHouseInt].origin

    usedMap.house[randHouseInt].relocate("random")

    # calculate value of map after new relocation
    mapValueAfter = usedMap.calculateValue()

    print(mapValueAfter)

    # replaces house if necessary
    if mapValueAfter < 0:
        counterForRelocation = 0
        while mapValueAfter < 0:
            usedMap.house[randHouseInt].relocate("random")
            mapValueAfter = usedMap.calculateValue()
            counterForRelocation += 1
            if counterForRelocation > relocateIterations:
                usedMap.house[randHouseInt].relocate(coord1)
                mapValueAfter = usedMap.calculateValue()

    if mapValueAfter <= mapValue:
        print("map is not better")
        usedMap.house[randHouseInt].relocate(coord1)
        mapValueAfter = usedMap.calculateValue()
        print("new value after relocate: {}".format(str(mapValueAfter)))

    startCounter += 1

    yValues.append(mapValueAfter)
    xValues.append(startCounter)

    # calculate value
    print("mapvalue After: " + str(mapValueAfter))

    print()

    if startCounter >= maxIterations:
        return usedMap
    else:
        return hillclimberRandomRelocateRecursive(usedMap, startCounter, maxIterations, relocateIterations, xValues, yValues)


def hillclimberRandomRelocate(usedMap, maxIterations, relocateIterations, xValues, yValues, goABitBack, houseTypes):

    if goABitBack:
        lastYValues = []
        savedMapValues = []

    gB = False

    for iteration in range(maxIterations):
        # calculate mapvalue
        mapValue = usedMap.calculateValue()
        # print("mapvalue before: " + str(mapValue))

        # get random house
        randHouseInt = randint(0, len(usedMap.house) - 1)

        # get coordinates from house randHouseInt
        coord1 = usedMap.house[randHouseInt].origin
        usedMap.house[randHouseInt].relocate("random")

        # calculate value of map after new relocation
        mapValueAfter = usedMap.calculateValue()

        # use the fallback way
        if goABitBack:
            if iteration >= goABitBack:
                lastYValues.remove(lastYValues[0])
                averageLastYValues = sum(lastYValues) / len(lastYValues)

                if lastYValues[-1] == averageLastYValues:
                    # revert map to save as JSON and then make it great again, turn on
                    mapValue = 0

                    # revert map to save as JSON and then make it great again, turn on
                    coord2 = usedMap.house[randHouseInt].origin
                    usedMap.house[randHouseInt].relocate(coord1)
                    JSONMapValue = usedMap.calculateValue()
                    usedMap.saveJSON(SAVE_MAP_LOC + "\\alg", str(JSONMapValue))
                    usedMap.house[randHouseInt].relocate(coord2)
                    savedMapValues.append(JSONMapValue)

        # relocate the house if the map is not better
        if mapValueAfter <= mapValue or doesItTouchForHc(usedMap.house[randHouseInt], usedMap.house):
            counterForRelocation = 0
            while True:
                usedMap.house[randHouseInt].relocate("random")
                mapValueAfter = usedMap.calculateValue()
                counterForRelocation += 1
                if mapValueAfter > mapValue and not doesItTouchForHc(usedMap.house[randHouseInt], usedMap.house):
                    break
                if counterForRelocation >= relocateIterations:
                    usedMap.house[randHouseInt].relocate(coord1)
                    break
            # print("subiterations used: " + str(counterForRelocation))

        mapValueAfter = usedMap.calculateValue()

        yValues.append(mapValueAfter)
        xValues.append(iteration)

        if goABitBack:
            lastYValues.append(mapValueAfter)

        # calculate value
        # print("mapvalue After: " + str(mapValueAfter))

        if iteration % 128 == 0:
            print("iteration: " + str(iteration))

    if goABitBack:

        # print(savedMapValues)
        bitBackValue = max(savedMapValues)

        if bitBackValue > mapValueAfter:
            usedMap.loadJSON(SAVE_MAP_LOC + "\\alg", str(bitBackValue), houseTypes, False)
            # print(max(savedMapValues), usedMap.calculateValue())
            yValues.append(bitBackValue)
            xValues.append(maxIterations)


def randomMapAlgorithm(tries, houseTypeList, xValues, yValues):

    # initialize counter, map, fill map and get value
    counter = 0
    bestMap = Map()
    fillMapWithRandomNonCollidingHouses(bestMap, houseTypeList)
    bestMapValue = bestMap.calculateValue()

    while True:

        # make empty map and fill it
        emptyMap = Map()
        fillMapWithRandomNonCollidingHouses(emptyMap, houseTypeList)

        # calculate values of two maps
        emptyMapValue = emptyMap.calculateValue()

        counter += 1

        # check which map to keep
        if emptyMapValue > bestMapValue:

            bestMap = emptyMap
            bestMapValue = emptyMapValue

        yValues.append(bestMapValue)
        xValues.append(counter)

        if counter % 128 == 0:
            print("iteration: " + str(counter))

        # return if counter has reached the amount of tries
        if counter >= tries:
            return bestMap


def fillMapWithRandomNonCollidingHouses(usedMap, houseTypeList):

    # fill map with houses
    for i in range(SELECTED_HOUSE_COUNT):
        ht = houseTypeList[i]
        usedMap.addHouse(ht, (0, 0), 0, "random_positions", "non_colliding")


def twoHouseSwitcher(usedMap, maxIterations, xValues, yValues, additiveXvalue):


    for iteration in range(maxIterations):

        mapValue = usedMap.calculateValue()

        # get two random houses
        randHouseIntOne = randint(0, len(usedMap.house) - 1)
        randHouseIntTwo = 0

        # check if its not the same house type
        while True:
            randHouseIntTwo = randint(0, len(usedMap.house) - 1)
            if usedMap.house[randHouseIntOne].type.name != usedMap.house[randHouseIntTwo].type.name:
                break

        # swap houses
        swapHouses(usedMap, randHouseIntOne, randHouseIntTwo)

        # calculate value
        mapValueAfter = usedMap.calculateValue()

        # check if map is valid and if not undo
        if usedMap.house[randHouseIntOne].ringboundary.isWithin(usedMap.boundary) and \
           usedMap.house[randHouseIntTwo].ringboundary.isWithin(usedMap.boundary) and \
           mapValueAfter > mapValue and \
           not doesItTouchForHc(usedMap.house[randHouseIntOne], usedMap.house) and \
           not doesItTouchForHc(usedMap.house[randHouseIntTwo], usedMap.house):
            pass

        # swap houses back since it's movement was illegal
        else:
            swapHouses(usedMap, randHouseIntTwo, randHouseIntOne)
            mapValueAfter = mapValue

        # add values to x, y and last goABitBack y values
        yValues.append(mapValueAfter)
        xValues.append(iteration + additiveXvalue)


def doesItTouchForHc(house, houseList):

    # check if houses do touch
    otherBoundaries = [h.boundary for h in houseList if h is not house]
    return house.boundary.isTouchingTight(otherBoundaries)


def hillclimberRandomRelocateWithSimulatedAnnealing(usedMap, maxIterations, relocateIterations, xValues, yValues, beginTemperature, endTemperature, differentOrNot, whatTemperatureFunc):

    for iteration in range(maxIterations):
        # calculate mapvalue
        mapValue = usedMap.calculateValue()

        # get random house
        randHouseInt = randint(0, len(usedMap.house) - 1)

        # get coordinates from house randHouseInt
        coord1 = usedMap.house[randHouseInt].origin
        usedMap.house[randHouseInt].relocate("random")

        # calculate value of map after new relocation
        mapValueAfter = usedMap.calculateValue()

        # relocate the house if the map is not better
        if mapValueAfter == -1 or doesItTouchForHc(usedMap.house[randHouseInt], usedMap.house):
            subIteration(usedMap, coord1, randHouseInt, relocateIterations)
            mapValueAfter = usedMap.calculateValue()

        if mapValueAfter < mapValue and mapValueAfter > 0:

            # use simulated annealing for worse values
            rand = random()
            shortening = mapValueAfter - mapValue
            temperature = temperatureFunction(whatTemperatureFunc, beginTemperature, iteration, endTemperature, maxIterations)
            # acceptationChanceDifferent = e ** ((shortening + (maxIterations - iteration)) / temperature)
            acceptationChance = e ** (shortening / temperature)

            # print("acc: " + str(acceptationChance))
            # print("shortening: " + str(shortening))
            # print("temp: " + str(temperature))

            if acceptationChance < rand:
                usedMap.house[randHouseInt].relocate(coord1)

        mapValueAfter = usedMap.calculateValue()
        yValues.append(mapValueAfter)
        xValues.append(iteration)

        if iteration % 128 == 0:
            print("iteration: " + str(iteration))


def temperatureFunction(which, T0, i, Tn, N):

    if which == "L":
        Ti = T0 - i * (T0 - Tn) / N
        return Ti

    elif which == "E":
        Ti = T0 * (Tn / T0) ** (i/N)
        return Ti

    elif which == "S":
        Ti = Tn + (T0 - Tn) / (1 + e ** (0.3 * ((i - N) / 2)))
        return Ti

    else:
        return -1
    # elif which == "G":


def subIteration(usedMap, coord1, randHouseInt, relocateIterations):

    # for simulated annealing to revert back
    counterForRelocation = 0
    while True:
        usedMap.house[randHouseInt].relocate("random")
        mapValueAfter = usedMap.calculateValue()
        counterForRelocation += 1
        if mapValueAfter != -1 and not doesItTouchForHc(usedMap.house[randHouseInt], usedMap.house):
            break
        if counterForRelocation >= relocateIterations:
            usedMap.house[randHouseInt].relocate(coord1)
            break

# Cherry


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

def cherryImproveSA(aMap, xValue, yValue):
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
    simanneal = True
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
                # moveToIdealPosition(house, aMap, increments, others)

            xValue.append(xValue[-1] + 1)
            yValue.append(aMap.calculateValue())


        if simanneal:
            simanneal = False
        else:
            simanneal = True

        # break if the map value is not improving anymore
        newValue = aMap.calculateValue()

        # highscore = 19000000
        # print at a certain point

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

def cherryImprove(aMap, xValue, yValue):
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
    # iterations = 0
    while(True):
        print("opnieuw")
        for house in reverse:
            # move 1 house to its move valuable position
            others = [h.boundary for h in aMap.house if h is not house]
            moveToIdealPosition(house, aMap, increments, others, xValue, yValue)

        # break if the map value is not improving anymore
        newValue = aMap.calculateValue()

        highscore = 19000000
        # print at a certain point
        # if printAt(aMap, newValue, highscore):
        #     highscore = newValue

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

def moveToIdealPosition(house, aMap, increments, otherBoundaries, xValue, yValue):
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
                xValue.append(xValue[-1] +1)
                yValue.append(aMap.calculateValue())

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



def main():

    it = []
    valuee = []

    for iii in range(2):

        housetypes = initHouseTypes(100)

        # generate correct type parameters
        housetypelist = []
        for ht in reversed(housetypes):
            n = round(ht.frequency * SELECTED_HOUSE_COUNT)
            housetypelist += [ht] * n

        # make a map
        yValues1 = []
        yValues2 = []
        yValues3 = []
        xValues = []
        xValues1 = []
        xValues2 = []
        xValues3 = []
        xValues4 = []
        yValues4 = []

        map1 = randomMapAlgorithm(ALG_ITERATIONS, housetypelist, xValues1, yValues1)

        incrementValue = xValues1[-1]
        xValues2.append(incrementValue)
        yValues2.append(yValues1[-1])

        # hillclimberRandomRelocate(map1, 5000, 5, xValues, yValues2, 200, housetypes)
        hillclimberRandomRelocateWithSimulatedAnnealing(map1, ALG_ITERATIONS, 4, xValues, yValues2, 60000, 9000, False, "L")

        for value in xValues:
            xValues2.append(value + incrementValue)
        xValues = []

        incrementValue = xValues2[-1]
        xValues3.append(incrementValue)
        yValues3.append(yValues2[-1])
        xValues.append(0)
        yValues3.append(map1.calculateValue())
        cherryImprove(map1, xValues, yValues3)
        for value in xValues:
            xValues3.append(value + incrementValue)
        xValues = []

        incrementValue = xValues3[-1]
        xValues4.append(incrementValue)
        yValues4.append(yValues3[-1])
        twoHouseSwitcher(map1, ALG_ITERATIONS, xValues, yValues4, 0)
        for value in xValues:
            xValues4.append(value + incrementValue)

        map1.addWater()

        plt.plot(xValues4, yValues4, color="orange")
        plt.plot(xValues3, yValues3, color="red")
        plt.plot(xValues2, yValues2, color="green")
        plt.plot(xValues1, yValues1, color="blue")

        print()

        value = map1.calculateValue()
        print("Total map value:", value)

        print("save to JSON")
        map1.saveJSON(SAVE_MAP_LOC, str(value))

        # legend algorithm:
        blue_patch = mpatches.Patch(color="blue", label="Random Algorithm")
        green_patch = mpatches.Patch(color="green", label="Simulated Annealing Exp.")
        red_patch = mpatches.Patch(color="red", label="Cherry Algorithm")
        orange_patch = mpatches.Patch(color="orange", label="Hillclimber Two House Switcher")

        plt.legend(handles=[blue_patch, green_patch, red_patch, orange_patch])

        mapValue = map1.calculateValue()

        plt.ylabel("Price")
        plt.xlabel("Iterations")
        plt.title("Algorithms")
        plt.savefig(SAVE_MAP_LOC + "\\" + NAME_PER_FILE + str(mapValue) + ".PNG")

        # map1.plot()
        plt.gcf().clear()
        it.append(iii)
        valuee.append(mapValue)

    plt.plot(it, valuee, color="blue")
    blue_patch = mpatches.Patch(color="blue", label="Algorithm")
    plt.legend(handles=[blue_patch])
    plt.ylabel("price single run")
    plt.xlabel("run")
    plt.savefig(SAVE_MAP_LOC + "\\ALL_FOR_40" + ".PNG")


if __name__ == "__main__":
        main()
