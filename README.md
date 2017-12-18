# Amstelhaege
This heuristics case is about the construction of a new residential area, which will need to be as profitable as it can be. A configuration of 20, 40 and 60 houses will be tested. These number of houses, and the amount they yield, are static. The houses can, however, gain additional value according to their free space. Free space is defined by the minimal distance to reach (the wall of) another house. The score of a map is defined as the sum of the prices of all houses, so needless to say, the more free space a house gains, the more valuable it, and the entirety of the map, becomes.

There is only one slight complication, the residential area will need to be filled in with a variety of house types, three to be exact, the family home, the bungalow, and the mansion. These house types all vary in frequency, surface occupancy, price, value gained per meter of free space, and mandatory free space. These numbers are, however, all given, static values.

The Amstelhaege case is quite a peculiar case compared to other cases. Not only
is the state space tremendously large (in the order of 10^88), but the sheer number of options to place
even one house(around 50000), makes it so most non-random algorithms, like depth / breath first, are meaningless.

That's why we decided to write a multitude of algorithms. By taking a wide number of approaches, and afterwards comparing the results, we'll compensate for the lack of precision.

To find high map scores / map values, houses will need to be placed and relocated. Hillclimber / Greedy algorithms are excellent contestants for this type of behavior. We've designed two hillclimbers. Both start out with a random, correct map or a previously created map. Both also edit a house, look if the map becomes more valuable, and undo's the edit if the map became less valuable. The first algorithms edits houses by taking precise steps, which we've called the "StepMover". The other one, titled "RandomMover", you've guessed it, moves the house to a completely random (correct) location.

We've also used an unconventional algorithm to solve this case, that we've simply dubbed, "The Unorthodox Algorithm". It can be seen as a greedy hillclimber, which uses local constraints to slowly push the lowest possible map value up, and checks if it is still possible to create a map with these local constraints.

So in total, three main algorithms are used:
**StepMover (Greedy and Plant propagation)**
**RandomMover  (Greedy and Simulated Annealing)**
**Unorthodox**

Further explanation of these algorithms can be found in their corresponding folders. The algorithms can also be used in conjunction. For example, the unorthodox algorithm can create a very good map, one the StepMover can improve even further by carefully moving a couple of houses.

## Getting Started


#### algorithms
    this folder holds all algorithms
#### algorithms/dependencies
    this package holds the used class structure, the given data, all third party dependencies.
#### results
    this folder contains experimentation and results of those algorithms, structured respectively towards the algorithm folder
#### Saves
    this folder acts as a storage for maps we deemed valuable to keep around, or just to show in between steps of certain algorithms
#### Rhino
    this is a 3D visualization we used in addition to mathplotlib. It can read saved jsons, and plot them dynamically and real-time in a 3d environment

## BEST RESULTS
by using the unorthodox algorithm in conjunction with the stepmover with simulated annealing, we got some of our best results:

20 houses:
    19.100.000 milion
    [image]

40 houses:
    24.000.000 milion
    [image]

60 houses:
    33.140.000 milion
    [image]

### Requirements
* **matplotlib 2.1.0**
* **os 16.1**
* **sys 29.1**
* **random 9.6**
* **numpy 1.14.1**

## Versioning
* **Atom 1.22.1**
* **GitHub**
* **Python 3.6.4**

for additional visualization
* **Rhino 5 **
* **Grasshopper 0.9.0076**

## Authors
*Beunhaas Architects*
* **Tara Elsen**
* **Christiaan Wewer**
* **Jos Feenstra**

# Acknowledgment
We would like to thank our Tech Assist Bart van Baal for guiding us throughout this project, and Course Daan van den Beg
