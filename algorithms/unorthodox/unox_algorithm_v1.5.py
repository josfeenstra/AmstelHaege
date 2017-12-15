"""
NAME    jos's Algorithm

AUTHORS jos feenstra

DESC    MAKING THE MAP DANCE

TODO
        are constraints satified

OPLOSMETHODE:
- UNORTODOX:
    1. bouw een sterke kaart via unorthodox
    2. gebruik simulated annealing & greedy hillclimbers
        - gebuikt house swapper
        - gebruik step mover

- ORTHODOX:
    1. hillclimb algorithm cycle



water:
    constraints relaxation

"""

from dependencies.helpers import *

# choose 0, 1 or 2 to get 20, 40 or 60 ho   uses
SELECTED_HOUSE_COUNT = HOUSE_COUNT[2]

# runtime controllers
MACRO_LIMIT = 650
LIMIT_MAP_REBUILT = 10000
LIMIT_HOUSE_RELOCATE = 300

# algorithm controls
START_AT = 240
# PRINT_AT = 1

# Path to save json files
jsonPATH = "C:\\Users\\Jos\\GitHub\\UrbanPlanning\\Rhino\\json"
jsonNAME = "josBest60"

"""
build a correct random map
"""
def main():

    housetypes = initHouseTypes(1000)

    # generate correct type parameters
    housetypelist = []
    for ht in reversed(housetypes):
        n = round(ht.frequency * SELECTED_HOUSE_COUNT)
        housetypelist += [ht] * n

    # init sets of plottable data
    ortodoxMapValuesSet = []
    unortodoxMapValuesSet = []
    allMapItsSet = []

    # ringpriority options
    ringPriorities = [[NONE, NONE,    1],  # USA
                      [NONE,    4,    1],  # BRITAIN
                      [   3,    2,    1],  # EUROPE
                      [   1,    1,    1]]  # RUSIA
    #
    # ringPriorities = [[NONE, NONE,    1],  # ONLY mansions
    #                   [NONE,    1, NONE],  # ONLY bungalows
    #                   [   1, NONE, NONE]]  # ONLY family homes

    # ringPriorities = [[NONE,    1,    1],  # EXCLUDE mansions
    #                   [NONE,    4,    1],  # EXCLUDE bungalows
    #                   [   3,    2,    1],  # EXCLUDE family homes

    ringPriorities = [[NONE , NONE,    1]]  # a certain division

    color        = ['-g'  , '-r' , '-c' , '-b' ]
    colorstriped = [ 'g--', 'r--', 'c--', 'b--']

    # save accidental best scores separately
    global_best_score = 0
    bestMap = Map()
    if not bestMap.loadJSON(jsonPATH, "bestestst.txt", housetypes, False):
        # if highscore cant be loaded, make sure to not overwrite high score
        global_best_score = 10000000
    else:
        global_best_score = bestMap.calculateValue()

    # loop through all ringPriorities
    fig, ax = plt.subplots()

    for distID, rp in enumerate(ringPriorities):

        best_score = 0

        # make a new map
        map1 = Map()

        # fill map for first time
        for i in range(SELECTED_HOUSE_COUNT):

            # get current housetype
            ht = housetypelist[i]
            map1.addHouse(ht, (0,0), 0, "random_positions", "non_colliding")

        # instanciate ringdata values
        map1.setHouseData(rp)
        theNextToDelete =   2

        # plottable data
        ortodoxMapValues = []
        unortodoxMapValues = []
        allMapIts = []
        iterations = []

        # keep increasing the best house
        for i in range(MACRO_LIMIT):

            # smart ring increase process
            selected = map1.selectAHouseBasedUponSomething(rp)
            houseSelected = map1.house[selected]
            houseSelected.changeRingsBy(1)

            # just continue if the map iteration has been made before
            if i < START_AT:
                continue

            # keep track of counter
            relocatecounter = 0

            # all House Boundaries Minus houseSelected
            otherBounds = [h.boundary for h in map1.house if h is not houseSelected]

            # if it does not fit
            if houseSelected.ringboundary.isTouching(otherBounds):

                # try to rebuild the entire map, if that fails, error
                print("rebuilding map. Iteration: {}".format(i))
                mapIterations = map1.rebuild(LIMIT_MAP_REBUILT, LIMIT_HOUSE_RELOCATE)
                allMapIts.append(mapIterations)

                # mapiterations ran out of steam, decide if we should quit or adapt
                if mapIterations <= -1:

                    # fix the map, then continue
                    map1.rebuild(LIMIT_MAP_REBUILT * 2, LIMIT_HOUSE_RELOCATE)

                    break

                    # if theNextToDelete == 0:
                    #     print("we're done!!")
                    #
                    #     # make sure the map quits with a valid map
                    #     map1.rebuild(LIMIT_MAP_REBUILT * 10, LIMIT_HOUSE_RELOCATE)
                    #     break
                    #
                    # # else, exclude mansions / bungalows
                    # print("excluding mansions/bungalows...")
                    # map1.excludeFromHouseData(theNextToDelete)
                    # #
                    # # some annealing
                    # for house in map1.house:
                    #     if house.type.integer == theNextToDelete:
                    #         house.changeRingsBy(-2)
                    #
                    # theNextToDelete -= 1

                    # reset map iterations
                    mapIterations = 0

            else:
                allMapIts.append(0)

            # keep track of the iteration
            print("iterations: {}".format(i))

            # # store map values
            mapVal = map1.calculateValue()
            ortodoxMapValues.append(mapVal)
            unortodoxMapValues.append(map1.calculateValueEstimate())
            iterations.append(i)

            # update for rhino visualisation
            # map1.addWater()
            map1.saveJSON(jsonPATH, jsonNAME)
            # map1.waterBody.clear()

            # if the map
            if mapVal > global_best_score:
                global_best_score = mapVal
                print("HIGH SCORE: {}".format(global_best_score))
                map1.saveJSON(jsonPATH, "bestestst.txt")

        # plot the data
        plt.plot(iterations, ortodoxMapValues, color[distID])
        plt.plot(iterations, unortodoxMapValues, colorstriped[distID])
        # map1.plot()

    plt.show()

    #
    # npIterations = np.array(iterations)
    # npAllMapIts = np.array(allMapIts)
    #
    # plt.plot(npIterations, npAllMapIts, '-g')
    #
    # plt.show()


    # cherry(map1, 1000)
    # orthodox(map1, 101010,10100,100)
    # if something
    #     simAnnealing(map1, 1000, 100)
    #



if __name__ == "__main__":
    main()
