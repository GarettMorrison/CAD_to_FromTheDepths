import json
import numpy as np
import scipy
from stl import mesh
from matplotlib import pyplot as plt
import pickle as pkl
import random

MAKE_SCATTER_PLOT = False

FILE_NAME = 'hull'
# FILE_NAME = 'cube'

# Load example blueprint
blueprint = json.load(open('ExampleVehicles/SINGLE_BLOCK_TEST.blueprint', 'r'))
def printJsonRecursive(fooDict, level):
	for foo in fooDict:
		for ii in range(level): print('   ', end='')
		if type(fooDict[foo]) == dict:
			print(f"{foo}:")
			printJsonRecursive(fooDict[foo], level+1)
		else:
			print(f"{foo}:{fooDict[foo]}")
printJsonRecursive(blueprint['Blueprint'], 0)

# Load constants
constants = pkl.load(open('constants/constants.pkl', 'rb'))
rotations = constants['rotations']
vertices = constants['vertices']

# Load block IDs
MATERIAL_NAME = 'Metal'
blockIDs = json.load(open('constants/block_ids.json', 'r'))
nameIdDict = {blockIDs[foo]['Name']:foo for foo in blockIDs}

# Init arbitrary defaults for itemdictionary
ItemDictionary = {"554": "e63040c9-0027-4fd3-be30-67fe3e950140"}
ItemDictIdxStart = 1200

blockVerticesByIdx = {}
blockNamesByIdx = {}
blockSizesByIdx = {}

validBlockIDCount = 0
for fooBlock in vertices:
	fullName = f"{MATERIAL_NAME} {fooBlock}"

	if fullName not in nameIdDict:
		print(f"Error: Unable to match {fullName}")
		continue
	
	blockIdx = int(validBlockIDCount + ItemDictIdxStart)
	validBlockIDCount += 1

	blockID = nameIdDict[fullName]

	blockSize = blockIDs[blockID]['SizeId']
	
	# maxBlockSize = 100
	# if blockSize > maxBlockSize:
	# 	print(f"Skipping {fullName} as size > {maxBlockSize}")
	# 	continue

	# if 'transition' in fullName:
	# 	print(f"Dropping transition block {fullName}")
	# 	continue

	ItemDictionary[str(blockIdx)] = blockID

	blockVerticesByIdx[blockIdx] = vertices[fooBlock]
	blockNamesByIdx[blockIdx] = fooBlock




outputPoints = pkl.load(open(f"processing/{FILE_NAME}_vox.pkl", 'rb'))



# Mirror points
shape = outputPoints.shape
mirrorPts = np.zeros((shape[0], 2*shape[1], shape[2]), dtype=np.int16)

setPoints = np.array(np.where(outputPoints == 1))
setPoints[1] += shape[1]
mirrorPts[*setPoints] = 1
setPoints[1] = 2*shape[1] - setPoints[1]
mirrorPts[*setPoints] = 1


# # Apply a little voxel smoothing
# adjacentPointCount = scipy.ndimage.convolve(mirrorPts, np.ones((3, 3, 3)))

# # for foo, cnt in zip(*np.unique(adjacentPointCount, return_counts=True)): print(f"{foo}:{cnt}")
# mirrorPts[np.where(adjacentPointCount < 9)] = 0
# mirrorPts[np.where(adjacentPointCount > 9)] = 1



def set_axes_equal(ax):
    """
    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    """

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

# Export just cubes
blockIDS = []
blockPlacements = []
blockRotations = []
blockColors = []


for fooPt in zip(*np.where(mirrorPts == 1)):
		blockIDS.append(600)
		blockPlacements.append(f"{fooPt[1]},{fooPt[2]},{fooPt[0]}")
		blockRotations.append(0)
		blockColors.append(0)

blueprint['ItemDictionary'] = {
	"554": "e63040c9-0027-4fd3-be30-67fe3e950140",
	"600": "ab699540-efc8-4592-bc97-204f6a874b3a",
}

blueprint['Blueprint']['BlockIds'] = blockIDS
blueprint['Blueprint']['BLP'] = blockPlacements
blueprint['Blueprint']['BLR'] = blockRotations
blueprint['Blueprint']['BCI'] = blockColors

blueprint['Blueprint']['BlockCount'] = len(blockPlacements)
blueprint['Name'] = 'TEST_BLOCKS'
blueprint['Blueprint']['ItemNumber'] = 554

json.dump(blueprint, open(f"output/{FILE_NAME}_JUST_CUBES.blueprint", 'w'), indent=2)




# Calculate boolean array of all vertex positions
vertexSet = np.zeros(np.array(mirrorPts.shape)+1, dtype=np.uint64)
vertexSet[:-1, :-1, :-1] = mirrorPts
vertexCalcKernel = np.zeros((3, 3, 3))
vertexCalcKernel[:-1, :-1, :-1] = 1

vertexSet = scipy.ndimage.convolve(vertexSet, vertexCalcKernel)
vertexSet[*np.where(vertexSet > 0)] = 1



# Convert set of vertices to uints
def encodeVertices(inArr, xLen = 2):
	shape = (xLen, 2, 2)
	outArr = np.zeros(inArr.shape, dtype=np.uint64)[:1-xLen, :-1, :-1]
	inArrShape = inArr.shape

	for fooPt in zip(*np.where(np.zeros(shape) == 0)):
		bitIndex = fooPt[2] + fooPt[1]*2 + fooPt[0]*4
		outArr += pow(2, bitIndex) * inArr[
			fooPt[0]:inArrShape[0] - shape[0] + 1 + fooPt[0], 
			fooPt[1]:inArrShape[1] - shape[1] + 1 + fooPt[1], 
			fooPt[2]:inArrShape[2] - shape[2] + 1 + fooPt[2],
		]
	return outArr


# Hard coded because screw this rotation encoding
# I just want to play my silly little boat game
rotationSet = [
	# Forward
	[
		(0, 1, 0), 
		(0, 18, 12, 16)
	],
	
	# Backward
	[
		(0, 1, 2), 
		(2, 17, 14, 19)
	],
	
	# Left
	[
		(0, 1, 1), 
		(3, 23, 16, 21)
	],
	
	# Right
	[
		(0, 1, -1), 
		(1, 20, 13, 22)
	],
	
	# Up
	[
		(0, 2, -1), 
		(10, 11, 8, 9)
	],
	
	# Down
	[
		(0, 2, 1), 
		(4, 7, 6, 5)
	]
]

# Arrays to rotate through
outputBlockIDs = np.zeros_like(mirrorPts, dtype=np.int16)
outputRotations = np.zeros_like(mirrorPts, dtype=np.uint8)

testArr = np.zeros((3, 3, 3), dtype=np.uint8)
testArr[0, 0, 0] = 1


for settingBlockLen in range(7, 0, -1):
	for faceRotationData in rotationSet:
		faceRotation = faceRotationData[0]
		faceOutRotations = faceRotationData[1]

		print(f"{settingBlockLen} : {faceRotation}")
		# Just rotate entire reference and output arrays instead of doing proper transformations for simplicity
		vertexSet = np.rot90(vertexSet, faceRotation[2], faceRotation[:2])
		targetVertexCodes = encodeVertices(vertexSet, settingBlockLen+1)
		outputBlockIDs = np.rot90(outputBlockIDs, faceRotation[2], faceRotation[:2])
		outputRotations = np.rot90(outputRotations, faceRotation[2], faceRotation[:2])

		for blockIdx in blockVerticesByIdx:
			fooVertexSet = np.array(blockVerticesByIdx[blockIdx], dtype=np.uint64)
			fooBlockLen = len(fooVertexSet) - 1

			if fooBlockLen != settingBlockLen: continue
			
			# for rotCnt, rotOut in zip(range(4), [0, 16, 12, 18]):
			for rotCnt, rotOut in zip(range(4), faceOutRotations):
				rotVertexSet = np.rot90(fooVertexSet, rotCnt, (1, 2))

				vertexCode = encodeVertices(rotVertexSet, fooBlockLen+1)[0,0,0]
			
				for fooPt in zip(*np.where(targetVertexCodes == vertexCode)):
					if outputBlockIDs[fooPt] != 0:
						blockingIdx = abs(outputBlockIDs[fooPt])
						# print(f"{blockNamesByIdx[blockIdx]} blocked by {blockNamesByIdx[blockingIdx]}")
						continue

					outputBlockIDs[fooPt[0]:fooPt[0]+fooBlockLen,fooPt[1], fooPt[2]] = -blockIdx
					outputBlockIDs[fooPt] = blockIdx
					outputRotations[fooPt] = rotOut

		testArr = np.rot90(testArr, faceRotation[2], faceRotation[:2])

		vertexSet = np.rot90(vertexSet, -faceRotation[2], faceRotation[:2])
		outputBlockIDs = np.rot90(outputBlockIDs, -faceRotation[2], faceRotation[:2])
		outputRotations = np.rot90(outputRotations, -faceRotation[2], faceRotation[:2])

if MAKE_SCATTER_PLOT:
	print(setPoints)
	ax = plt.figure().add_subplot(projection='3d')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	for fooIdx in np.unique(outputBlockIDs):
		if fooIdx <= 0: continue
		print(fooIdx)

		setPoints = np.where(outputBlockIDs == fooIdx)
		ax.scatter(*setPoints, label=blockNamesByIdx[fooIdx])

	set_axes_equal(ax)
	plt.legend()
	plt.show()

	# print(path)
	# exit()


# Export cubes and blocks
blockIDS = []
blockPlacements = []
blockRotations = []
blockColors = []

for fooPt in zip(*np.where(outputBlockIDs > 0)):
	blockIDS.append(outputBlockIDs[fooPt])
	blockPlacements.append(f"{fooPt[1]},{fooPt[2]},{fooPt[0]}")
	blockRotations.append(outputRotations[fooPt])
	blockColors.append(0)




# Need to modify (in ["Blueprint"])
# BlockIDS: What block is being place
# BLP: Placement of block (list of strings for some reason)
# BLR: Block rotation
# BCI: Block color I think

blueprint['ItemDictionary'] = ItemDictionary
blueprint['Blueprint']['BlockIds'] = [int(foo) for foo in blockIDS]
blueprint['Blueprint']['BLP'] = blockPlacements
blueprint['Blueprint']['BLR'] = [int(foo) for foo in blockRotations]
blueprint['Blueprint']['BCI'] = blockColors

blueprint['Blueprint']['BlockCount'] = len(blockPlacements)
blueprint['Name'] = 'TEST_BLOCKS'
blueprint['Blueprint']['ItemNumber'] = 554

json.dump(blueprint, open(f'output/{FILE_NAME}_marched.blueprint', 'w'), indent=2)

