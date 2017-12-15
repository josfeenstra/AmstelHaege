
from dependencies.helpers import *

# get arguments
houseTypes = initHouseTypes(100)
fileName = "31976880_cherrymover"
dirPath = "C:\\Users\\Jos\\GitHub\\UrbanPlanning\\Rhino\\json"

# make fill and plot the map
map1 = Map()
map1.loadJSON(dirPath, fileName, houseTypes, False)
map1.plot()
