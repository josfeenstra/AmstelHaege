README ABOUT ORTHODOX ALGORITHMS:

RANDOM ALGORITHM:

While(True):
    Make a new random map
    If new map is better than old map:
        Continue with new map
    Else:
        Continue old one

RANDOM HILLCLIMBER:

Input is an already created map.

While(True):
    Take a random house
    Put it in a random position
    While the position is invalid or the map is worse:
        Try placing house again
    If the map is still invalid:
        Revert map

RANDOM TWO HOUSE SWAPPER:

While(True):
    Take a random house
    Take another random house of another type
    Switch both houses
    While position is invalid or map is worse:
        revert
    If map is valid and better:
        Repeat with this map    

RANDOM HILLCLIMBER SPECIAL:

-random hillclimber with additional feature:
if a map does not improve after X iterations, it will accept a map with a valid lower value

STEPMOVER HILLCLIMBER (Also called cherry / wiggle algorithm):

While(True):
    For each house on map:
        increment = 32 meters
        Move north/ east/ south/ west by increment:
            If better map value & legal move:
                Update map
                Repeat
            Else:
                Same_map_value += 1
If Same_map_value => house
        Increment /= 2         (until it is 0.5 m)


SIMULATED ANNEALING:

three different temperature functions:

    Ti = T0 - i * (T0 - Tn) / N
    Ti = T0 * (Tn / T0) ** (i/N)
	Ti = Tn + (T0 - Tn) / (1 + e ** (0.3 * ((i - N) / 2)))
