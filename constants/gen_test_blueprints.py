import json
import numpy as np
from stl import mesh
from matplotlib import pyplot as plt
import pickle as pkl
from copy import deepcopy
import os

if not os.path.isdir('output'):
	os.makedirs('output')

def printJsonRecursive(fooDict, level=0):
	for foo in fooDict:
		for ii in range(level): print('   ', end='')
		if type(fooDict[foo]) == dict:
			print(f"{foo}:")
			printJsonRecursive(fooDict[foo], level+1)
		else:
			print(f"{foo}:{fooDict[foo]}")


# Generate blueprint that has every example block placed
blockIDs = json.load(open('constants/block_ids.json', 'r'))

# beam 4m : 47 : 1404

TARGET_MATERIAL = 'Metal'
outputBlocks = []
outputIdx = 1404 - 1099
for fooID in blockIDs:
	fooData = blockIDs[fooID]
	outputIdx += 1


	blockName = fooData['Name'][len(TARGET_MATERIAL)+1:] # Get just part of name that does not include material label
	blockSize = fooData['SizeId']

	if fooData['Material'] != TARGET_MATERIAL: continue
	if TARGET_MATERIAL !=  fooData['Name'][:len(TARGET_MATERIAL)]: continue
	# if blockSize > 1: continue


	print(f"{outputIdx}:   {blockSize}   {blockName} ")

	outputBlocks.append([blockName, outputIdx, blockSize, fooID])

def reformatJSON(fileName):
	loadBP = json.load(open(fileName, 'r'))
	json.dump(loadBP, open(fileName, 'w'), indent=2)

# reformatJSON("output/TEST_ADD_cmp.blueprint")



# Process test blocks
TestBlocks = json.load(open('ExampleVehicles/SINGLE_BLOCK_TEST.blueprint', 'r'))
for idx in range(len(TestBlocks['Blueprint']['BlockIds'])):
	blockID = TestBlocks['Blueprint']['BlockIds'][idx]
	BLP = TestBlocks['Blueprint']['BLP'][idx]
	BLR = TestBlocks['Blueprint']['BLR'][idx]
	BCI = TestBlocks['Blueprint']['BCI'][idx]

	fooBlockCode = TestBlocks['ItemDictionary'][str(blockID)]

	blockID_data = blockIDs[fooBlockCode]

	print(f"{blockID} : {fooBlockCode}     {blockID_data}")


# exit()

# Load example blueprint
origBluePrint = json.load(open('ExampleVehicles/SINGLE_BLOCK_TEST.blueprint', 'r'))
blueprint = deepcopy(origBluePrint)

# Need to modify (in ["Blueprint"])
# BlockIDS: What block is being place
# BLP: Placement of block (list of strings for some reason)
# BLR: Block rotation
# BCI: Block color I think
blockIDS = []
blockPlacements = []
blockRotations = []
blockColors = []

# ItemDictionary BlockID:Codes
ItemDictionary = {"554": "e63040c9-0027-4fd3-be30-67fe3e950140"}
ItemDictIdx = 554

blockNameArr = np.array([foo[0] for foo in outputBlocks])
outputIdxArr = np.array([foo[1] for foo in outputBlocks])
blockSizeArr = np.array([foo[2] for foo in outputBlocks])
fooIDArr = np.array([foo[3] for foo in outputBlocks])

# print(blueprint)
# blockIdx = 1444
# ItemDictionary[f'{blockIdx}'] = blueprint['ItemDictionary'][f"{blockIdx}"]


placePos = -1
for idx in np.argsort(blockNameArr):
	placePos += 1
	# if placePos%6 == 0: continue

	fooPt = [0, placePos, 0]
	blockIdx = int(outputIdxArr[idx] + ItemDictIdx)

	ItemDictionary[str(blockIdx)] = fooIDArr[idx]
	blockIDS.append(blockIdx)
	blockPlacements.append(f"{fooPt[1]},{fooPt[2]},{fooPt[0]}")
	blockRotations.append(0)
	blockColors.append(0)

	print(f"{blockNameArr[idx]}")


blueprint['Blueprint']['BlockIds'] = blockIDS
blueprint['Blueprint']['BLP'] = blockPlacements
blueprint['Blueprint']['BLR'] = blockRotations
blueprint['Blueprint']['BCI'] = blockColors
blueprint['ItemDictionary'] = ItemDictionary

print(ItemDictionary)

# blueprint['Blueprint']['designChanged'] = True
blueprint['Blueprint']['BlockCount'] = len(blockPlacements)
blueprint['Name'] = 'TEST_BLOCKS'
blueprint['Blueprint']['ItemNumber'] = 554

json.dump(blueprint, open('output/TEST_BLOCKS.blueprint', 'w'), indent=2)
json.dump(origBluePrint, open('output/INPUT.blueprint', 'w'), indent=2)




# Test rotation encoding
blockIDS = []
blockPlacements = []
blockRotations = []
blockColors = []


ItemDictionary = {
	"499": "e63040c9-0027-4fd3-be30-67fe3e950140",
	"1436": "c5550009-2b37-41ff-a788-d413b39376ae",
}

# Place a bunch of Metal triangle corner (left) (2m) to indicate rotation
for idx in range(24):
	fooPt = [0, idx*2, 0]

	blockIDS.append(1436)
	blockPlacements.append(f"{fooPt[1]},{fooPt[2]},{fooPt[0]}")
	blockRotations.append(idx)
	blockColors.append(0)

	print(f"Rot {idx}")


blueprint = deepcopy(origBluePrint)
blueprint['Blueprint']['BlockIds'] = blockIDS
blueprint['Blueprint']['BLP'] = blockPlacements
blueprint['Blueprint']['BLR'] = blockRotations
blueprint['Blueprint']['BCI'] = blockColors
blueprint['ItemDictionary'] = ItemDictionary

json.dump(blueprint, open('output/TEST_ROT.blueprint', 'w'), indent=2)

exit()
printJsonRecursive(origBluePrint)
print(f'\n\n\n\n\n')
for foo in blueprint['Blueprint']:
	print(f"\n----- {foo} -----")
	print(blueprint['Blueprint'][foo])
	print(origBluePrint['Blueprint'][foo])

foo = 'ItemDictionary'
print(f"\n----- {foo} -----")
print(origBluePrint[foo])
print(blueprint[foo])
