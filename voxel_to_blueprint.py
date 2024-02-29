import json
import numpy as np
from stl import mesh
from matplotlib import pyplot as plt
import pickle as pkl

# Save BPs here:
# /mnt/c/Users/garet/OneDrive/Documents/From The Depths/Player Profiles/Morjor/Constructables/Testing/GENERATED_BLUEPRINT.blueprint

# Load example blueprint
blueprint = json.load(open('ExampleVehicles/DIFF_LENS_2X.blueprint', 'r'))
def printJsonRecursive(fooDict, level):
	for foo in fooDict:
		for ii in range(level): print('   ', end='')
		if type(fooDict[foo]) == dict:
			print(f"{foo}:")
			printJsonRecursive(fooDict[foo], level+1)
		else:
			print(f"{foo}:{fooDict[foo]}")
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


outputPoints = pkl.load(open(f"output/voxel.pkl", 'rb'))




shape = outputPoints.shape
mirrorPts = np.zeros((shape[0], shape[1]*2, shape[2]), dtype=np.int16)

mirrorPts[:, shape[1]:, :] = outputPoints
mirrorPts[:, :shape[1], :] = np.flip(outputPoints, axis=1)
# setPoints = np.where(outputPoints == 1)[0]
# setPoints[0] += shape[0]
# mirrorPts[setPoints] = 1

# setPoints[0] = shape[0]*2 - setPoints[0]
# mirrorPts[setPoints] = 1

outPts = []

print(f"outputPoints:{np.sum(outputPoints)}/{outputPoints.shape[0]*outputPoints.shape[1]*outputPoints.shape[2]}")
print(f"mirrorPts:{np.sum(mirrorPts)}/{mirrorPts.shape[0]*mirrorPts.shape[1]*mirrorPts.shape[2]}")

for fooPt in np.swapaxes(np.array(np.where(mirrorPts == 1)), 1, 0):
	blockIDS.append(565)
	# blockPlacements.append(f"{xx},{yy},{zz}")
	blockPlacements.append(f"{fooPt[1]},{fooPt[2]},{fooPt[0]}")
	blockRotations.append(0)
	blockColors.append(0)
	outPts.append(fooPt)




blueprint['Blueprint']['BlockIDS'] = blockIDS
blueprint['Blueprint']['BLP'] = blockPlacements
blueprint['Blueprint']['BLR'] = blockRotations
blueprint['Blueprint']['BCI'] = blockColors
json.dump(blueprint, open('GENERATED_BLUEPRINT.blueprint', 'w'))

