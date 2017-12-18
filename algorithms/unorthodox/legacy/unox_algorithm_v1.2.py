"""
NAME    printSquare

AUTHORS Christiaan Wewer
        Tara Elsen
        jos feenstra        1196 95

DESC    STATE SPACE estimation calculation

NOTE    this thing is an example of how to use helpers
"""
"""
HEURISTICS NOTES

prefer placing houses with the same type together
    prefer placing houses which perfectly fit together
prefer placing houses on edges of other houses or water
prefer placing houses so they fit perfectly in AREA boundaries
prefer to place as much 'extra free space' off the edge of the AREA boundaries

group houses, consider them as 1 (moldable) puzzle piece

LOGBOEK
    Jos's HillCLimber Algorithm
    v 1.1:
        - add ring to best house
        - if it doesnt fit
            - random jump 1000 times until valid
                - if still not valid, crash

        NOTE: this doesnt work, the mansion keep on jumping, the family homes must move to make place for the large houses

    v 1.2:
        - add ring to best house
        - if ONE OF THE OTHER HOUSES DOES NOT FIT ANYMORE
            - random jump THEM 1000 times until valid
                - if still not valid, crash

        NOTE: this also doesnt work, if two mansions clash they still jump around alot



"""

# TODO turn main into hillclimber
# TODO save all values generated in .txt file
# TODO make an algoritm which determines which ring is the most valuable to add, with value in price / m2


from helpers import *

# choose 0, 1 or 2 to get 20, 40 or 60 houses
SELECTED_HOUSE_COUNT = 20 # HOUSE_COUNT[0]


"""
build a correct random map
"""
def main():
    housetypes = initHouseTypes(100)

    # generate correct type parameters
    housetypelist = []
    for ht in reversed(housetypes):
        n = round(ht.frequency * SELECTED_HOUSE_COUNT)
        housetypelist += [ht] * n

    # make a map
    map1 = Map()

    # add a number of houses to map
    for i in range(SELECTED_HOUSE_COUNT):

        # get current housetype
        ht = housetypelist[i]

        # the add house function which i want
        map1.addHouse(ht, (0,0), 0, "random_positions", "non_colliding")

    # add water to the map (TODO)
    # map1.addWater()

    # map1.expandRings()

    MACRO_LIMIT = 400
    MICRO_LIMIT = 10000
    #
    # # keep increasing the best house
    for i in range(MACRO_LIMIT):

        selected = map1.findHouseWithMostLandValueRingIncrease()
        houseSelected = map1.house[selected]
        houseSelected.changeRingsBy(1)

        # keep track of counter
        relocatecounter = 0

        # iterate through all houses

        for checkHouse in map1.house:

            # allHouseBoundariesMinusCheckHouse = []
            otherbounds = [h.boundary for h in map1.house if h.origin != checkHouse.origin]

            # if it does not fit
            if houseSelected.ringboundary.isTouching(checkHouse.boundary):
                succes = checkHouse.moveUntilValid(otherbounds, MICRO_LIMIT)
                if not succes:
                    print("ERROORORORORORORO")
                    print("houseClash:" + houseSelected.type.name + " and " + checkHouse.type.name)



        # once every 100 ringincreases, print map
        if (i % 30 == 0):
            print("iterations: {}".format(i))
            map1.plot()



    # print value of map
    value = map1.calculateValue()
    print()
    print("Total map value:", value)

    # draw the map a second time
    map1.plot()

if __name__ == "__main__":
    main()
