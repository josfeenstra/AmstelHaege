"""
NAME    mapvaluebounds.py

AUTHORS Jos Feenstra
        Christiaan Wewer

DESC    calculate the minimum and maximum possible map value

NOTE

"""
import sys
sys.path.append("..")
from dependencies.helpers import *
from dependencies.classes import HouseType, House, WaterBody, Rectangle, Map

# choose 0, 1 or 2 to get 20, 40 or 60 ho   uses
SELECTED_HOUSE_COUNT = HOUSE_COUNT[1]

# Path to save json files
jsonPATH = "C:\\Users\\Jos\\GitHub\\AmstelHaegeNew\\Saves\\json"
jsonNAME = "upperboundstatespace20"

# how many times rings overlap, estimate
FACTOR = 4

# max. iterations (for damage control)
MACRO_LIMIT = 1000

def main():

    # total area of the map is needed as an
    total_area = AREA[0] * AREA[1] * FACTOR

    #
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

    # loop through all ringPriorities
    fig, ax = plt.subplots()

    # make a new map
    map1 = Map()

    # fill map for first time
    for i in range(SELECTED_HOUSE_COUNT):

        # get current housetype
        ht = housetypelist[i]
        map1.addHouse(ht, (0,0), 0, "random_positions", "non_colliding")

    # get lowerbound
    lower = map1.calculateValueEstimate()

    # keep increasing the best house
    for i in range(MACRO_LIMIT):

        # smart ring increase process
        selected = map1.findHouseWithMostLandValueRingIncrease()

        houseSelected = map1.house[selected]
        houseSelected.changeRingsBy(1)

        ringarea = houseSelected.ring.actualArea
        total_area -= ringarea
        # print(map1.house[selected].ring.actualArea)
        if total_area <= 0:
            print("mapvalue range with {} houses.".format(SELECTED_HOUSE_COUNT))
            print("LOWERBOUND: € {:,}".format(lower))
            print("UPPERBOUND: € {:,}".format(map1.calculateValueEstimate()))
            print("(iterations: {})".format(i))
            break



if __name__ == "__main__":
    main()
