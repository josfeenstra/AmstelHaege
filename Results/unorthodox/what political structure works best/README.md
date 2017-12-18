## experimentation
Beunhaas Architects
by Tara, Christiaan, and Jos

It became clear that in order to make the best maps, the additional free space in between houses needs to be maximized. But there's a twist,
the value which is gained by giving a house additional free space varies greatly between the different types of houses. We wanted to test what distribution of additional free space would be the most valuable.

the unorthodox algorithm (more on the functionality of the algorithm later), can be used to create different distributions of free space, or rings. we inserted the following distributions:

- [1, 1, 1] Equality:                  All houses gain rings equally
- [3, 2, 1] Leaning towards mansions:  For every ringincrease of the family homes, the bungalows gain 2, and the mansions gain 3.
- [0, 0, 0] Classic:                   Assign rings based upon value increase, divided by land taken.             
- [0, 0, 1] The One Percent:           Assign rings only to the mansions        
