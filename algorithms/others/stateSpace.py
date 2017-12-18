from dependencies.helpers import *
SELECTED_HOUSE_COUNT = 20

def main():

    # get housetypelist
    housetypes = initHouseTypes(100)
    housetypelist = []
    for ht in reversed(housetypes):
        n = round(ht.frequency * SELECTED_HOUSE_COUNT)
        housetypelist += [ht] * n

    # generate variables
    stateSpace = 0
    housesArea = 0

    # iterate through houses
    for houseOption in range(SELECTED_HOUSE_COUNT):
        houseNum = housetypelist[houseOption].integer
        houseArea = (SITE[houseNum][0] + BASE_RING[houseNum]) *  (SITE[houseNum][1] + BASE_RING[houseNum])
        housesArea += houseArea
        actuallyTotalArea = AREA[0] * AREA[1]
        if houseOption == 0:
            stateSpace = actuallyTotalArea - housesArea
        else:
            stateSpace *= actuallyTotalArea - housesArea

    print("Statespae: {}".format(stateSpace))

if __name__ == "__main__":
    main()