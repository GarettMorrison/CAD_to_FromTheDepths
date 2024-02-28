import json
import numpy as np\

blueprint = json.load(open('ExampleVehicles/DIFF_LENS_2X.blueprint', 'r'))
# blueprint = json.load(open('ExampleVehicles/SINGLE_BLOCK_TEST.blueprint', 'r'))


def printJsonRecursive(fooDict, level):
	for foo in fooDict:
		for ii in range(level): print('   ', end='')
		if type(fooDict[foo]) == dict:
			print(f"{foo}:")
			printJsonRecursive(fooDict[foo], level+1)
		else:
			print(f"{foo}:{fooDict[foo]}")


# printJsonRecursive(sb_blueprint, 0)
printJsonRecursive(blueprint['Blueprint'], 0)




# Need to modify (in ["Blueprint"])
# BlockIDS: What block is being place
# BLP: Placement of block (list of strings for some reason)
# BLR: Block rotation
# BCI: Block color I think

blockIDS = []
blockPlacements = []
blockRotations = []
blockColors = []

outputScale = 30
outputPoints = np.array((outputScale, outputScale, outputScale), dtype=np.int16)


for xx in range(outputScale):
	for yy in range(outputScale):
		for zz in range(outputScale):
			if np.sqrt(np.power(xx - outputScale/2, 2) + np.power(yy - outputScale/2, 2) + np.power(zz - outputScale/2, 2)) < outputScale/2:
				blockIDS.append(1444)
				blockPlacements.append(f"{xx},{yy},{zz}")
				blockRotations.append(0)
				blockColors.append(0)

blueprint['Blueprint']['BlockIDS'] = blockIDS
blueprint['Blueprint']['BLP'] = blockPlacements
blueprint['Blueprint']['BLR'] = blockRotations
blueprint['Blueprint']['BCI'] = blockColors

json.dump(blueprint, open('GENERATED_BP.blueprint', 'w'))