"""
NAME    classes.py

AUTHOR  Jos Feenstra
        Tara Elsen
        Christiaan Wewer

DESC    contains the classes:
        - HouseType
        - House
        - WaterBody
        - Rectangle
        - Map

NOTE

    IN HINDSIGHT, we shouldve made waterbody and house an extention of rectangle,
    instead of nesting respective rectangles in the ".boundary". Right now, to many
    lines of code will have to be rewritten in order to fix this. This approach
    would have come with its own complications, but the end result would be more clear

"""
# dependent upon the methods, constances and libaries in helpers
from dependencies.helpers import *

################################################################################

class HouseType(object):
    """
    Housetype Class
    """
    def __init__(self, aName, aFrequency, aValue, aSite, aBaseRing, aRingIncrement, MaxRingIt, aColour, anInteger):

        # base values
        self.integer   = anInteger
        self.name      = aName
        self.frequency = aFrequency
        self.value     = aValue
        self.site      = aSite
        self.baseRing  = aBaseRing
        self.ringInc   = aRingIncrement
        self.colour    = aColour

        # calculated values
        self.width     = self.site[0]
        self.height    = self.site[1]
        self.area      = self.width * self.height
        self.landValue = self.value / self.area
        self.ringValue = round(self.ringInc * self.value)

        # do not calculate rings if the basering is incorrect
        if self.baseRing - 1 < 0:
            raise print("ERROR: Ring Creation Error")

        # instanciate cummulative variables
        cumArea        = self.area
        cumValue       = self.value
        cumLandValue   = self.landValue

        # fill ring list with Ring objects
        class Ring:
            pass
        self.ring = list()

        # iterate starting from basering, ending at Max Ring Iteration
        for ringWidth in range(self.baseRing, MaxRingIt):

            # turn r into Ring object
            r = Ring()

            # calc land value in  / m2, and calc other attributes
            r.ringWidth = ringWidth                  # synoniem
            r.x = ringWidth * 2 + self.width
            r.y = ringWidth * 2 + self.height
            r.area = r.x * r.y - cumArea

            # the first ring is part of the house, so it yields no value
            r.value = 0
            if ringWidth != self.baseRing:
                r.value = self.ringValue
            r.landValue = round(r.value / r.area, 1)

            # increase the cummilative values, and add the current values to r
            cumArea += r.area
            r.cumArea = cumArea

            cumValue += r.value
            r.cumValue = cumValue

            cumLandValue = round(cumValue / cumArea)
            r.cumLandValue = cumLandValue

            # add Ring object r to list ring
            self.ring.append(r)

        # calc house's lower- and upperbounds of x and y coordinates
        self.xLower = self.ring[0].ringWidth
        self.yLower = self.ring[0].ringWidth
        self.xUpper = AREA[0] - self.ring[0].ringWidth - self.width
        self.yUpper = AREA[1] - self.ring[0].ringWidth - self.height

    def printRingInfo(self):
        print()
        print(self.name)
        printstr = "| ring: {:2}   x: {:2}   y: {:3}   area: {:5}  landValue: {:5}  cumArea: {:6}  cumValue: {:7}   cumLandValue: {:5} |"
        print((len(printstr) - 4) * "-")
        for r in self.ring:
            print(printstr.format(r.ringWidth, r.x, r.y, r.area, r.landValue, r.cumArea, r.cumValue, r.cumLandValue ))
        print((len(printstr) - 4) * "-")

################################################################################

class House(object):
    """
    House Class
    """
    def __init__(self, aType, aCoord, addRings):
        self.type = aType
        self.addRings = addRings

        # shortest distance to another house, will be added later
        self.shortest = 0

        # assign either a random coordinate, or assign given coordinate
        if aCoord == "random":
            # randomize numbers, with 0.5 precision
            random_x = round(uniform(self.type.xLower, self.type.xUpper) * 2) / 2
            random_y = round(uniform(self.type.yLower, self.type.yUpper) * 2) / 2

            self.origin = (random_x, random_y)
        else:
            self.origin = aCoord

        # update geometic info
        self.update()

    def update(self):
        # calculate additional geometric information, based on init's current value
            # EXAMPLE a fam.house with 3 add.rings gives a ringWidth of 5.

        # select current ring
        self.ring = self.type.ring[self.addRings]

        # house geometry rep. boundary
        self.boundary = Rectangle(self.origin, self.type.width, self.type.height)

        # move houseOrigin diagonal to create ringOrigin
        vector = (-1 * self.ring.ringWidth, -1 * self.ring.ringWidth)
        ringOrigin = moveCoord(self.origin, vector)

        # house ring rep. boundary
        self.ringboundary = Rectangle(ringOrigin, self.ring.x, self.ring.y)

        # make some synonimes for lazy use
        self.coord = self.origin

        if ORTHODOX:
            # recalculate distances to other houses,
            pass

    def move(self, vector):

        # add vector and origin coordinate, and update other values accordingly
        self.origin = moveCoord(self.origin, vector)
        self.update()

    def relocate(self, aCoord, *edges):
        """ probably the same as moveTo """

        if aCoord == "random":
            # pick a random coordinate, with type coord bounds and 0.5 precision
            self.origin = randomCoord((self.type.xLower, self.type.yLower),
                                      (self.type.xUpper, self.type.yUpper))

        elif aCoord == "random_on_edge": # TODO
            # oh boy here we go TODO placement is missing a few possibilites!!!
            # RANDOMNESS IS NOW INCORRECT: algorithm first randomly chooeses edge, then coord, TODO should be joined endevor
            edges = edges[0]
            picked = np.random.choice(range(len(edges)))

            # pick a random edge & coord on that edge
            edge = edges[picked]

            # the highest ring width should be the minimum distance the house should move
            ringSelf = self.ring.ringWidth
            ringOther = edge[2]
            ring = max(ringSelf, ringOther)

            # TODO something has to be done here
            coordLowBound  = (edge[0][0], edge[0][1])
            coordHighBound = (edge[1][0], edge[1][1])
            coord = randomCoord(coordLowBound, coordHighBound)

            # test
            # print("ring = {}".format(ring))
            # print("coord = {}".format(coord))

            # # determine direction, and change origin coord accordingly
            direction = edge[3]
            if direction == "T": # coord should move up
                newcoord = (coord[0], coord[1] + ring)
            elif direction == "D": # coord should move down
                newcoord = (coord[0], coord[1] - (ring + self.type.height))
            elif direction == "L": # coord should move left
                newcoord = (coord[0] + ring, coord[1])
            elif direction == "R": # coord should move right
                newcoord = (coord[0] - (ring + self.type.width), coord[1])

            # make special exeptions for placement on map edges
            elif direction == "Tm": # coord should move up
                newcoord = randomCoord((self.type.xLower, self.type.yUpper), (self.type.xUpper, self.type.yUpper))
            elif direction == "Dm": # coord should move down
                newcoord = randomCoord((self.type.xLower, self.type.yLower), (self.type.xUpper, self.type.yLower))
            elif direction == "Lm": # coord should move left
                newcoord = randomCoord((self.type.xLower, self.type.yLower), (self.type.xLower, self.type.yUpper))
            elif direction == "Rm": # coord should move right
                newcoord = randomCoord((self.type.xUpper, self.type.yLower), (self.type.xUpper, self.type.yUpper))
            else:
                # something went wrong
                print("ERROR: random_on_edge: incorrect direction given, cannot continue...")
                while(True):
                    pass

            # assign the coord
            self.origin = newcoord

        else:
            # assign the given coord
            self.origin = aCoord

        # update house data
        self.update()

    def changeRingsBy(self, increment):
        # change the |Additional Ring| value by |Increment|, error if addrings becomes negative (not allowed)
        # quit if addRings would become negative
        if self.addRings + increment < 0:
            print("ERROR: additional rings cannot become negative")
            return

        # add the increment, and update values
        self.addRings += increment
        self.update()

    def moveUntilValid(self, listOfRectangles, limit):

        # if it does not fit
        iteration = 0
        while(iteration < limit):

            # if self isnt touching anything anymore
            if not self.ringboundary.isTouching(listOfRectangles):

                # its correct
                return True

            # prepare for next iteration
            self.relocate("random")
            iteration += 1

        # if code falls through here, could not place house
        return False

    def isWithinMap(self):
        if (self.type.xLower <= self.origin[0] <= self.type.xUpper and
            self.type.yLower <= self.origin[1] <= self.type.yUpper):
            # house is within map
            return True

        # else, its not
        return False

################################################################################

class WaterBody(object):
    """
    Water Class
    """
    def __init__(self, aCoord, aSurface, aRatio): #coord as tuple (x, y), surface as m2,
        # STATIC create ratio's array, and an array sorted by probability
        # 0.25 , 0.50, 0.75, 1, 2, 3, 4
        highN = [i/1 for i in range(2, RATIO_UPPER_BOUND + 1)]
        lowN  = [i / RATIO_UPPER_BOUND for i in range(1, RATIO_UPPER_BOUND + 1)]
        self.ratioList = lowN + highN
        ratioSortedList = highN + lowN


        # assign either a random ratio, or assign given ratio
        if aRatio == "random":
            # pick a random number from the list
            self.ratio = choice(self.ratioList)
        else:
            # test ratio
            if not (RATIO_LOWER_BOUND <= aRatio <= RATIO_UPPER_BOUND):
                print("ERROR: ratio out of bound: <{}, {}>".format(RATIO_LOWER_BOUND, RATIO_UPPER_BOUND))
                return
            self.ratio = aRatio

        # assign either a random coordinate, or assign given coordinate
        if aCoord == "random":
            # randomize numbers, with 0.5 precision, upperbound not precise, will need to check if valid move
            random_x = round(uniform(0, AREA[0]) * 2) / 2
            random_y = round(uniform(0, AREA[1]) * 2) / 2
            self.origin = (random_x, random_y)
        else:
            self.origin = aCoord

        # test surface
        if (aSurface <= 0):
            print("ERROR: surface must be non-zero positive")
            return
        self.surface = aSurface

        # update geometric information
        self.update()

    def update(self):

        # TODO fix rounding stuff, floats are slow and inaccurate

        # update width & height
        self.width  = sqrt(self.surface / self.ratio)
        self.height = sqrt(self.surface * self.ratio)

        # update rectangle information
        self.boundary = Rectangle(self.origin, self.width, self.height)

        # lower and upper bounds could be done for coord's sake

    def changeLocation(self, aCoord):
        """
        the following three methods change 1 of the 3 initial values and
        updates all other values accordinly
        """
        # assign either a random coordinate, or assign given coordinate
        if aCoord == "random":
            # randomize numbers, with 0.5 precision, upperbound not precise, will need to check if valid move
            random_x = round(uniform(0, AREA[0]) * 2) / 2
            random_y = round(uniform(0, AREA[1]) * 2) / 2

            self.origin = (random_x, random_y)
        else:
            self.origin = aCoord
        self.update()

    def changeRatio(self, aRatio):

        if aRatio == "random":
            # pick a random number from the list
            self.ratio = choice(self.ratioList)
        else:
            # test ratio
            if not (RATIO_LOWER_BOUND <= aRatio <= RATIO_UPPER_BOUND):
                print("ERROR: ratio out of bound: <{}, {}>".format(RATIO_LOWER_BOUND, RATIO_UPPER_BOUND))
                return
            self.ratio = aRatio
        self.update()

    def changeSurface(self, aSurface):
        if (aSurface <= 0):
            print("ERROR: surface must be non-zero positive")
            return
        self.surface = aSurface
        self.update()

################################################################################

class Rectangle(object):
    """
    rectangle class

    this class is key to the speed of all algorithms, edit with caution

    Methods:
    toString()                              # turn self. information into string
    isTouching(|rectangle / rectangles|)    # test if self is touching ||
    isWithin(|rectangle / rectangles|)      # test if self is completely within ||
    """
    def __init__(self, OriginCoord, width, height):

        self.width = width
        self.height = height

        self.x1 = OriginCoord[0]
        self.y1 = OriginCoord[1]
        self.coord1 = (self.x1, self.y1)

        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.coord2 = (self.x2, self.y2)

    def toString(self):
        """
        turn some of rectangles variables to string to test
        """
        return ("Rectangle.coord1: {} \nRectangle.coord2: {} \n".format(
               self.coord1,
               self.coord2)
               )

    def isWithin(self, listOfRectangles):
        """
        return true if self is completely within list of rectangles
        """
        # if list is emtry, rectangle is not within it
        if not listOfRectangles:
            return False

        # make it so a single rectangle also works
        if not isinstance(listOfRectangles, Iterable):
            listOfRectangles = [listOfRectangles]

        # get self' 4 boundary coordinates
        bound_coords = [(x, y) for x in [self.x1, self.x2]
                               for y in [self.y1, self.y2]]

        # calculate per boundary coordinate
        for bound_coord in bound_coords:
            # per rectangle in given list of rectangles
            for rec in listOfRectangles:

                # rename bound coord for the sake of clear names
                x = bound_coord[0]
                y = bound_coord[1]

                # test conditions
                if not rec.x1 <= x < rec.x2 or not rec.y1 <= y < rec.y2:
                    return False

        # if code falls down till this part, position is correct
        return True

    def isTouchingTight(self, listOfRectangles):
        """
        return true if self is touching any part of list of rectangles
        """
        # empty list means its not overlapping
        if not listOfRectangles:
            return False

        # make it so a single rectangle also works
        if not isinstance(listOfRectangles, Iterable):
            listOfRectangles = [listOfRectangles]

        # for better readability
        A = self

        # rectangle B (other)
        for B in listOfRectangles:
            # both 'an X coord' and 'a Y coord' of B need to be within the respective bounds of A if they touch.
            # this can be writen shorter, but this is the most readable

            if ((A.x1 <= B.x1 <= A.x2      # one of my x's are within your x's
            or   A.x1 <= B.x2 <= A.x2
            or   B.x1 <= A.x1 <= B.x2      # one of your x's are within my x's
            or   B.x1 <= A.x2 <= B.x2)
            and
                (A.y1 <= B.y1 <= A.y2      # one of my y's are within your y's
            or   A.y1 <= B.y2 <= A.y2
            or   B.y1 <= A.y1 <= B.y2      # one of your y's are within my y's
            or   B.y1 <= A.y2 <= B.y2)):
                return True

        # if code falls down till this part, none of the rectangles are overlapping with self
        return False

    def isTouching(self, listOfRectangles):
        """
        return true if self is touching any part of list of rectangles
        """
        # empty list means its not overlapping
        if not listOfRectangles:
            return False

        # make it so a single rectangle also works
        if not isinstance(listOfRectangles, Iterable):
            listOfRectangles = [listOfRectangles]

        # for better readability
        A = self

        # rectangle B (other)
        for B in listOfRectangles:
            # both 'an X coord' and 'a Y coord' of B need to be within the respective bounds of A if they touch.
            # this can be writen shorter, but this is the most readable

            if ((A.x1 < B.x1 < A.x2      # one of my x's are within your x's
            or   A.x1 < B.x2 < A.x2
            or   B.x1 < A.x1 < B.x2      # one of your x's are within my x's
            or   B.x1 < A.x2 < B.x2)
            and
                (A.y1 < B.y1 < A.y2      # one of my y's are within your y's
            or   A.y1 < B.y2 < A.y2
            or   B.y1 < A.y1 < B.y2      # one of your y's are within my y's
            or   B.y1 < A.y2 < B.y2)):
                return True

        # if code falls down till this part, none of the rectangles are overlapping with self
        return False

    def getEdges(self, ringWidth):

        # order: TDLR
        self.edges = [[(self.x1, self.y2), (self.x2, self.y2), ringWidth, "T"],  # top range
                      [(self.x1, self.y1), (self.x2, self.y1), ringWidth, "D"],  # bottom/down range
                      [(self.x2, self.y1), (self.x2, self.y2), ringWidth, "L"],  # left range
                      [(self.x1, self.y1), (self.x1, self.y2), ringWidth, "R"]]  # right range
        return self.edges

    def getEdgesFlipped(self, ringWidth):

        # order: DTRL, the direction is flipped
        self.edges = [[(self.x1, self.y2 + 1), (self.x2, self.y2 + 1), ringWidth, "D"],  # top range
                      [(self.x1, self.y1 - 1), (self.x2, self.y1 - 1), ringWidth, "T"],  # bottom/down range
                      [(self.x2 - 1, self.y1), (self.x2 - 1, self.y2), ringWidth, "R"],  # right range
                      [(self.x1 + 1, self.y1), (self.x1 + 1, self.y2), ringWidth, "L"]]  # left range
        return self.edges

    def getBoundCoords(self):

        # only recalculate if it is meaningful??? check this later
        self.bound_coords = [(x, y) for x in [self.x1, self.x2]
                                    for y in [self.y1, self.y2]]

        return self.bound_coords

    def getShortestDistanceOld(self, otherBoundaries):

        # instanciate with a large number, so the first one will always become shorter
        shortest = 300

        # get corners from boundaries
        houseCorners = self.getBoundCoords()
        otherCorners = []
        for boundary in otherBoundaries:
            if boundary is not self:
                for coord in boundary.getBoundCoords():
                    otherCorners.append(coord)

        # per coord of the selected house
        for hc in houseCorners:

            # now, check distances hc vs. otherCoords
            x1 = hc[0]
            y1 = hc[1]
            allDistancesWithoutRoot = []
            for other in otherCorners:

                # get second coord info
                x2 = other[0]
                y2 = other[1]

                # calculate distance to this point using pythagoras
                disx = abs(x1 - x2)
                disy = abs(y1 - y2)

                # TODO test the thing BART talked about
                if   self.y1 <= y2 <= self.y2:
                    # x distance = complete distance, still need power(disy) for the sake of speed
                    allDistancesWithoutRoot.append(disx * disx)
                elif self.x1 <= x2 <= self.x2:
                    # y distance = complete distance, still need power(disy) for the sake of speed
                    allDistancesWithoutRoot.append(disy * disy)
                else:
                    allDistancesWithoutRoot.append(
                        disx * disx  + disy * disy
                    )

            # calculate square root part separately, to
            foundShortest = sqrt(min(allDistancesWithoutRoot))
            if foundShortest < shortest:
                shortest = foundShortest

        # return the shortest shortest
        return shortest

    def getShortestDistance(self, allCorners):

        shortest = -1
        selfCorners = self.getBoundCoords()
        self.distanceList = []
        # per set of 4 coord of the houses of the entire map
        for setCorners in allCorners:

            # skip a beat if the set == my own set
            if selfCorners == setCorners:
                continue

            # now, check distances hc vs. otherCoords
            sixteenDistances = []

            # per selfs corner coordindate in self.set
            for selfC in selfCorners:

                # per other corner coordindate in set
                for otherC in setCorners:

                    # calculate distance to this point using pythagoras
                    disx = abs(selfC[0] - otherC[0])
                    disy = abs(selfC[1] - otherC[1])

                    # make sure that if possible, the distance from wall to wall is calculate
                    if   self.y1 <= otherC[1] <= self.y2:
                        # x distance = complete distance, still need power(disy) for the sake of speed
                        sixteenDistances.append(disx * disx)
                    elif self.x1 <= otherC[0] <= self.x2:
                        # y distance = complete distance, still need power(disy) for the sake of speed
                        sixteenDistances.append(disy * disy)
                    else:
                        sixteenDistances.append(disx * disx  + disy * disy)


            # calculate square root part separately, to speed up process
            # foundshortest is the minimum distance in between self and other
            foundShortest = min(sixteenDistances)

            # add it to the list of distances
            self.distanceList.append(foundShortest)

        # print(self.distanceList)

        # return the shortest distance from the list
        return sqrt(min(self.distanceList))

################################################################################

class Map(object):
    """
    Map class which holds houses

    METHODS AND THEIR USE:
    Map(coord1=(0,0), coord2=(AREA))                 # defines the surface area of the map
    addHouseStupid(type, coord, rings)               # this could be deleted, its a raw way of adding a house, without any further calculations
    addHouse(type, coord, rings, *args)              # create a house in a certain smart version, for options, see the method description
    plot()                                           # plot all significant geometric information loaded into the map using mathplotlib
    expandRings()                                    # expand the rings to their maximum allowed expantion, in other words, calculate value after this for actual map value
    addWater()                                       # water add algorithm, using random locations and configurations. It tries to squeeze in water in between existing geometry
    calculateValueEstimate()                         # estimate map value using the currently placed rings
    calculateValue()                                 # the actual value of the map is calculated here, regardless of rings present
    getEdges(ringWidth)                              # used by FitInOnEdge algorithm, dont delete, but unimportant
    findHouseWithMostLandValueRingIncrease()         # THIS IS THE RING ADDER, it returns the index of the house with the best next ring
    areConstraintsSatisfied()                        # a final check, returns true if all map conditions are met
    rebuild( RUNTIME_LIMIT_MAP, RUNTIME_LIMIT_HOUSE) # place all houses on the map again with a certain guaranteed free space, and try to make them fit
    saveJSON(self, nameOfFile)                       # save map to a json file with a certain name, can be used to make a real time rhino visualisation
    """

    def __init__(self, coord1=(0,0), coord2=AREA):
        # init base values
        self.coord1 = coord1
        self.coord2 = coord2
        self.width  = coord2[0] - coord1[0]
        self.height = coord2[1] - coord1[1]

        # init lists to fill with objects
        self.house = []
        # houseIndex = 0
        self.waterBody = []

        # init a boundary for collision testing
        self.boundary = Rectangle(self.coord1, self.width, self.height)

    def addHouseStupid(self, aType, aCoord, addRings):
        """
        add a [aType] house to the map at [aCoord], with [addrings] rings
        """

        # simple way of creating a house
        self.house.append(House(aType, aCoord, addRings))

    def addHouse(self, aType, aCoord, addRings, *options):
        """
        add a [aType] house to the map at [aCoord], with [addrings] rings
        the following options are usable:
            ["non_colliding"]
                pick random house locations until the position is valid.
            ["random_positions"]
                place house at a random starting location
        """

        # apply options
        LoopUntilValid = False
        if any(option == "non_colliding" for option in options):
            # print("make a house without colliding")
            LoopUntilValid = True
        if any(option == "random_positions" for option in options):
            # print("make house at a random location")
            h = (House(aType, "random", addRings))
        else:
            # print("make a house in ordinary fashion")
            h = (House(aType, aCoord, addRings))

        # directly append h if we dont need to check for valid position
        if not LoopUntilValid:
            self.house.append(h)
        else:
            # if we do need to check if placement is valid
            relocateCounter = 0
            MAX_ITERATIONS = 50000
            # list of squares to test with
            allRings = [house.ringboundary for house in self.house]

            while(True):
                # make iteration upper bound
                if relocateCounter > MAX_ITERATIONS:
                    print("Cannot place house...")
                    return 1
                # check if the h's house boundary is touching any existing ringboundary
                if h.boundary.isTouching(allRings):
                    # incorrect placement
                    relocateCounter += 1
                    h.relocate("random")
                else:
                    # correct placement
                    self.house.append(h)
                    # print("Times Relocated: ", relocateCounter)
                    break

    def expandRings(self):
        """
        Expand all rings to their maximum possible value.
        """
        # NOTE this code might also work with coordinate distances, distance to edge etc, and then floor() the minimal answer

        print("\n Expanding rings...")

        # make a new list of houses
        newHouses = []

        # per imbedded hosue
        for house in self.house:
            # TODO do while loop?????
            houses = self.house

            # count number of rings added
            added_rings = []

            # make new house with 1 more ring
            hCurrent = house
            hNew = (House(house.type, house.origin, house.addRings + 1))

            # save boundaries of all embedded houses
            allBoundaries = [testhouse.boundary for testhouse in self.house if testhouse.origin != house.origin]

            # the new ring is valid when its completely within map boundaries,
            # and not any house can be touching this new ringboundary
            # hNew.ringboundary.isWithin(self.boundary) and
            while(not any([houseboundary.isTouching(hNew.ringboundary)
                            for houseboundary in allBoundaries])):
                # if new ring is possible, replace hCurrent with hNew, and repeat
                added_rings.append(hNew.addRings)

                hCurrent = hNew
                hNew = (House(hCurrent.type, hCurrent.origin, hCurrent.addRings + 1))

            # if it is not possible, quit loop
            # print(" rings added: ", added_rings)
            newHouses.append(hCurrent)

        # after all loopnig:
        self.house = newHouses

    def shrinkRings(self):
        """
        shrink all additional ring sizes back to zero
        """
        print("\n shrinking rings...")

        # per imbedded hosue
        houses = self.house
        for house in houses:

            # this will set the number back to 0
            house.changeRingsBy(house.addRings * -1)

    def addWater(self):
        """
        Add water to the map.
        """
        # calculate water m2 needed
        waterArea = WATER_PERCENTAGE * AREA[0] * AREA[1]

        # feedback
        print()
        print("adding {} m2 of water...".format(waterArea))

        # determines chosen TestSizes in while loop. change to make the algorithm more accurate / slow
        DECREMENT = round(-0.05 * waterArea)
        STARTING_SIZE = round(STARTING_WATER_ITERATION_SIZE * waterArea)

        # init values to keep track of
        bodiesLeft = MAX_BODIES
        waterLeft = waterArea

        # init waterBody, to prevent memory overload
        wb = WaterBody("random", STARTING_SIZE, "random")

        # and testSize * waterArea >= 1 / MAX_BODIES;
        testSize = STARTING_SIZE
        while (testSize * bodiesLeft >= waterLeft and waterLeft != 0):  # macro while loop

            # test current area size
            wb.changeSurface(testSize)

            # iteration values
            MAX_TRIES = 1000
            tries = 0
            succeeded = False
            while(tries < MAX_TRIES):    # micro while loop
                # if the waterbody isnt touching any houses or other bodies, and is within the map
                if (not wb.boundary.isTouchingTight([h.boundary for h in self.house]) and not
                        wb.boundary.isTouchingTight([w.boundary for w in self.waterBody]) and
                        wb.boundary.isWithin(self.boundary)):
                    # the waterbody is correct
                    succeeded = True
                    break

                # else, change the values of wb, and try again
                wb.changeRatio("random")
                wb.changeLocation("random")
                tries += 1

            if succeeded:
                # success micro while loop: update counters, save wb, and build a 'new' wb
                bodiesLeft -= 1
                self.waterBody.append(wb)
                waterLeft -= testSize
                if waterLeft < testSize:
                    testSize = waterLeft

                if waterLeft <= 0:
                    # sucess macro while loop:
                    print("Water added.")
                    return True

                # no decrement, macro while loop should try to fit the same size somewhere else
                wb = WaterBody("random", testSize, "random")
            else:
                # make the wb smaller
                testSize += DECREMENT

        # if macro while loop runs out, water could not be placed...
        print("Failed to add water...")
        self.waterBody.clear()
        return False

    def calculateValue(self):
        """
        Determine the value of the land.
        """
        total = 0

        # calculate all corners houses of the map
        allCorners = [house.boundary.getBoundCoords() for house in self.house]
        # allBoundaries = [house.boundary for house in self.house]

        # per house
        for house in self.house:

            # calculate the shortest distance between a boundary and other boundaries
            shortest = house.boundary.getShortestDistance(allCorners)
            
            # the additional space is determined by subtracting the mandatory personal space
            addPersonalSpace = shortest - house.type.baseRing

            # assign distance to house, so it can be referenced
            house.shortest = shortest

            # check if map conditions are met (this method of map doubles as a validation checker)
            if addPersonalSpace < 0:
                house.shortest = 0
                return -1

            # now, calculate the value of this house
            ringPrice = round((house.type.ringValue * addPersonalSpace))
            housePrice = house.type.value

            # and update total with this
            total += ringPrice + housePrice

        # return the accumilation of all those values
        return total

    def calculateValueEstimate(self):
        """
        Determine the value of the land.
        """
        total = 0
        # per house
        for house in self.house:
            # add house's cummilative value of the current ring
            total += house.ring.cumValue

        return total

    def getEdges(self, ringWidth):
        """
        returns the edge list of the map
        the map edges work differently, to this method
        TODO: this is fucking stupid right now, needs to be fixed in less stupid fashion
        """
        # order: TDLR
        return [[(0,0), (0,0), 0, "Tm"],  # top range
                [(0,0), (0,0), 0, "Dm"],  # bottom/down range
                [(0,0), (0,0), 0, "Lm"],  # left range
                [(0,0), (0,0), 0, "Rm"]]  # right range

    def findHouseWithMostLandValueRingIncrease(self):

        housedata = []
        # iterate through houses
        for index, house in enumerate(self.house):
            # get the landValue of the next ring
            pair = (house.type.ring[house.addRings + 1].landValue, index)

            # add data to list
            housedata.append(pair)

        # sort
        # print(housedata)
        selected_house = max(housedata, key=operator.itemgetter(0))
        # print(selected_house)

        return selected_house[1]

    def setHouseData(self, listOfratiorepresentatives):
        """
        initiate the housetypes list, for easier access to all types.
        set the data for the value increaser
        """

        self.houseTypes = [house.type.integer for house in self.house]
        self.houseData = []
        for typeID in self.houseTypes:
            dataStart = listOfratiorepresentatives[typeID]
            self.houseData.append(dataStart)

    def selectAHouseBasedUponSomething(self, listOfratiorepresentatives):
        """
        returns a house index of the house with the largest 'something'

        the 100000 inellegant, could be improved

        listOfratiorepresentatives:
        [3,2,1] = for every 1 ringincrease of fhome, increase 3 rings on mansion
        [10000,10000,1] = only increase rings on mansions
        [1,1,1] = equal ringincreases on all of them

        """

        # pick the smallest value from the housedata list
        # selectedID = min(xrange(len(self.houseData)), key=values.__getitem__)
        selectedID = np.argmin(self.houseData)

        # get that houses' type
        typeID = self.houseTypes[selectedID]

        # update housedata based upon the type and the ratiorepresentative
        self.houseData[selectedID] += listOfratiorepresentatives[typeID]

        # return the id
        return selectedID

    def excludeFromHouseData(self, typeToExclude):
        """
        exclude all houses of typeToExclude from the housedata set, in other words,
        dont let them increase their rings anymore
        """

        for i in range(len(self.houseData)):

            # exclude by increasing the data value to an incredibly high amound that will never be reached
            if self.house[i].type.integer == typeToExclude:
                self.houseData[i] = A_VERY_HIGH_INT

    def setHouseData(self, listOfratiorepresentatives):
        """
        initiate the housetypes list, for easier access to all types.
        set the data for the value increaser
        """

        self.houseTypes = [house.type.integer for house in self.house]
        self.houseData = []
        for typeID in self.houseTypes:
            dataStart = listOfratiorepresentatives[typeID]
            self.houseData.append(dataStart)

    def areConstraintsSatisfied(self):
        # NOTE THIS IS REALLY SLOW, MEANT AS A LAST CHECK
        # NOTE this method judges the map based upon the current rings
        for house in self.house:

            # all houses with selection excluded, and waterbodies
            waterBounds = [wb.boundary for wb in self.waterBody]
            houseBounds = [house.boundary for h in self.house if house is not h]

            # check if this house is touching a body of water
            if house.boundary.isTouching(waterBounds):
                print("map not satisfied: houseTouchWater")
                return False

            # check if this house is touching another house
            if house.boundary.isTouching(houseBounds):
                print("map not satisfied: houseTouchHouse")
                return False

            # check if the house is outside of map boundaries
            if not house.isWithinMap():
                print("map not satisfied: houseWithin")
                return False

        # go through all waterbodies
        for waterBody in self.waterBody:

            # NOTE houses do not need to be checked, done before

            # all water with selection excluded
            otherWaterBounds = [wb.boundary for wb in self.waterBody if wb is not waterBody]

            # check if this body of water isnt touching other waterbodies
            if waterBody.boundary.isTouching(otherWaterBounds):
                print("map not satisfied: WaterTouch")
                return False

            # check if this body of water is not completely within the map
            if not waterBody.boundary.isWithin(self.boundary):
                print("map not satisfied: WaterWithin")
                return False

        # if code falls to this point, map is correct
        return True

    def rebuild(self, RUNTIME_LIMIT_MAP, RUNTIME_LIMIT_HOUSE):
        """
        rebuild the map in random fashion with 1000 tries.

        NOTE instantiating new houses for example a thousand times takes up
             alot of memory, so instead this algorithm moves houses around.
        """

        # try LIMIT amound of times
        iterationMap = 0
        while(iterationMap < RUNTIME_LIMIT_MAP):

            # create a quick way to go to the next map try
            nextMap = False

            # build list from newly placed houses to compare with
            compareBoundaries = []
            compareRingBoundaries = []
            edges = self.getEdges(0)
            iterationMap += 1

            # go trough all houses
            for house in self.house:

                # relocate regardless of correct or not
                house.relocate("random_on_edge", edges)
                iterationHouse = 0

                # while this house is incorrectly placed
                while(house.boundary.isTouching(compareRingBoundaries) or
                      house.ringboundary.isTouching(compareBoundaries) or
                      not house.isWithinMap()):

                    # if house iterations have reached their upper limit
                    if iterationHouse >= RUNTIME_LIMIT_HOUSE:
                        nextMap = True
                        break

                    # try a new position
                    iterationHouse += 1
                    house.relocate("random_on_edge", edges)

                # goto next map iteration
                if nextMap == True:
                    break

                # else house is correct, add it to comparrison list
                compareBoundaries.append(house.boundary)
                compareRingBoundaries.append(house.ringboundary)
                edges.extend(house.boundary.getEdges(house.ring.ringWidth))

            # goto next map iteration
            if nextMap == True:
                continue

            # else map is correct
            return iterationMap

        # if code falls though here, map could not be
        print("map.rebuild Runtime Error")
        return -1

    def plot(self):
        """
        plot the full map with all houses, implementing mathplotlib.
        """
        # TODO maybe draw borers

        # init figure and axes
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')

        # determine title and subtitles
        fig.suptitle('HEURISTICS: Amstelhaege', fontsize=14, fontweight='bold')

        # write subtitle based upon map's correctness
        value = self.calculateValue()
        if value == -1:
            print("map not satisfied: houseTouchHouse")
            ax.set_title("MAP IS INCORRECT", color='red')
        elif not self.areConstraintsSatisfied():
            ax.set_title("MAP IS INCORRECT | Map value: {}".format(value), color='orange')
        else:
            ax.set_title("Map value: {:,}".format(value))

        # add water to the map
        for body in self.waterBody:
            rec1 = mathplot_rectangle(body.boundary.coord1, body.boundary.width, body.boundary.height, 0, fc=WATER_COLOUR, alpha=0.5)
            ax.add_patch(rec1)

        # add houses to the map with rings
        for house in self.house:
            # create a normal mathplot rectangle for the house
            rec1 = mathplot_rectangle(house.boundary.coord1,
                                      house.boundary.width,
                                      house.boundary.height,
                                      0, fc=house.type.colour,
                                      edgecolor='k',linewidth=1)
            ax.add_patch(rec1)

            # create a rectangle with rounded corners for the distance to another house
            rec2 = FancyBboxPatch(house.boundary.coord1,
                                  house.boundary.width,
                                  house.boundary.height,
                                  boxstyle="round,pad=0.1",
                                  mutation_scale=house.shortest * 10,
                                  fc=house.type.colour,
                                  alpha=0.2)
            ax.add_patch(rec2)

        # determines how axis are drawn
        ax.set_xticks(np.arange(0, self.width, 10))
        ax.set_yticks(np.arange(0, self.height, 10))
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])

        # draw the board
        plt.show()

    def saveJSON(self, pathOfFile, nameOfFile):
        """
        pathOfFile should lead to the a folder containing the json
        nameOffile should be its name

        """
        # move to the right directory if needed
        if os.getcwd() is not pathOfFile:
            os.chdir(pathOfFile)

        # construct a dictonary of map data
        data = {}

        # add metadata
        data['map'] = []
        data['map'].append({
            'width': AREA[0],
            'height': AREA[1],
            'value': self.calculateValue()
        })

        # convert map's houses to json
        data['houses'] = []
        for house in self.house:
            data['houses'].append({
                'x1'  : house.origin[0],
                'y1'  : house.origin[1],
                'int' : house.type.integer,
            })

        # convert map's waterbodies to json
        data['water'] = []
        for water in self.waterBody:
            data['water'].append({
                'x1'      : water.boundary.x1,
                'y1'      : water.boundary.y1,
                'ratio'   : water.ratio,
                'surface' : water.surface
            })

        # store data in json file
        j = json.dumps(data, indent=4)
        f = open(nameOfFile, 'w')
        f.write(j)
        f.close()

    def loadJSON(self, pathOfFile, nameOfFile, housetypes, addWater):
        fullPath = pathOfFile + "//"+ nameOfFile

        #Read JSON data into the data variable
        if fullPath:
            with open(fullPath, 'r') as f:
                data = json.load(f)
                f.close()
        else:
            print("loading json failed, could not open path")
            return False

        # reset houses and waterbodies of map
        self.house.clear()
        self.waterBody.clear()

        # loop through jsons's house data elements
        for house in data["houses"]:
            x1 = house["x1"]
            y1 = house["y1"]
            ht = housetypes[house["int"]]

            # turn values into house object
            self.addHouseStupid(ht , (x1, y1), 0)

        # skip adding water if bool is false
        if not addWater:
            return True

        # loop through jsons's water data elements
        for water in data["water"]:
            x1 = water["x1"]
            y1 = water["y1"]
            ratio = water["ratio"]
            surface = water["surface"]
            newWaterBody = WaterBody((x1, y1), surface , ratio)

            self.waterBody.append(newWaterBody)

        return True
    #
    # def saveCSV(self):
    #
    #     file_name = "Saves/" + str(self.calculateValue()) + ".csv"
    #     with open(file_name, "w"):
    #         locationList = []
    #         for house in self.houses:
    #             row = [house.origin,, house.type.integer]
    #             locationList.append(row)
    #         for water in self.water:
    #             # 3 is representative of water
    #             row = [water.boundary.coord1, water.boundary.coord2, 3]
    #             locationList.append(row)
    #         writer = pandas.DataFrame(locationList, columns=["co-ordinate set 1", "co-ordinate set 2", "object ID"])
    #         writer.to_csv(file_name, index=False)
    #         print("location list" + str(locationList))

################################################################################
