EXPERIMENTATION_README.MD

Experimentation Orthodox:

In order to produce good experimentation results, the algorithms have divided into three groups.

1. Start algorithm: 
	-Random Sampling

2. Effective score increasing algorithms:
	-Regular Hillclimbing
	-Hillclimbing Special
	-Simulated Annealing

3. Final map optimization algorithms:
	- Wiggle Hillclimber (cherry algorithm)
	- Random Two House Swapper Hillclimber
	
Logic behind this division is:
	-random sampling produces mostly maps around 12M and 13M, which is low pricing
	-regular Hillclimbing, Hillclimbing Special and Simulated Annealing do change the map as a whole
	-Wiggle Hillclimber and Random Two House Swapper Hillclimber do only optimize house postitions without changing the map as a whole (see readme on algorithms)
	-We cannot try all combinations since Beunhaas Architects has limited computing power

	
The maps chosen to experiment on, where always 20 house maps. 
This has been decided because these maps are the fastest to optimize since Beunhaas Architects has limited computing power.
The best working combinations can be tried on 40 and 60 house maps.

Excel file with analyzation: OUTCOME_HC_HCS_RANDOM_SIM.xlsx

STEPS:

Generate 40 random maps by random sampling, 1K iterations:
	-Average Result: 12149609
	-Max Result: 12802830
	-Min Result: 11857080
	
	
Take best random map and compare all "Effective score increasing algorithms" for 40 times. 
For all algorithms 5K iterations have been used.
In order for a map to continue to a "final map optimization algorithm" it has to have a value of 17M or higher.

	Hillclimber:
		-Average Result: 16435302
		-Max Result: 17274270
		-Min Result: 15627030
		-for graphs and maps see: HILLCLIMBING_20 folder
		-2 17M+ maps
	
	Hillclimber special:
		-Average Result: 16435302
		-Max Result: 17274270
		-Min Resutl: 15627030
		-for graphs and maps see: HILLCLIMBING_SPECIAL_20 folder
		-2 17M+ maps
	
	For Simulated Annealing 3 temperature functions have been used as described in the algorithm readme.
	
		Used Values:
		T0 = 60K
		Tn = 9K
		
		If the random generated value is lower than the acceptance probability, the lower map will be accepted.
		For temperature, acceptance probability per iteration and acceptance probability by shortening see the file: FUNctions_sim_an.xlsx
		
		Linear temperature function:
			-Average Result: 16275375
			-Max Result: 16913790
			-Min Result: 15653430
			-0 17M+ maps
		
		Exponential temperature function:
			-Average Result: 16400438
			-Max Result: 17195730
			-Min Result: 15816120
			-2 17M+ maps
			
		Sigmoid temperature funciton:
			-Average Result: 15980039
			-Max Result: 16704360
			-Min Result: 15184200
			0 17M+ maps

	For final map optimization algorithms there have been tried two setups.
		-First Wiggle Hillclimber and as second Random Two House Swapper Hillclimber
		-First Random Two House Swapper Hillclimber and as second Wiggle Hillclimber
	
	Only maps with a value of 17M or higher have been used.
		
		cherry to two house swapper
		average:	17808287
		max:	18078840
		min:	17425110

		best results.
		this scenario has been used for 60 houses as well and 40 too.
		
		

		

	
	



