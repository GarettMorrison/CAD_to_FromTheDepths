import json
import numpy as np
from stl import mesh
from matplotlib import pyplot as plt
import pickle as pkl
from copy import deepcopy
import os


def loadTxt(fileName, fooType):
	readFile = open(fileName, 'r')
	
	outData = {}
	currLabel = None
	currData = []
	for foo in readFile.readlines():
		if foo[0] == '#': continue
		
		if len(foo) < 2:
			if currLabel != None:
				# print(currData)
				rawArr = np.array(currData)
				outArray = np.zeros((len(currData), 2, 2), dtype=np.int8)
				# I encoded block_vertices in a way that was convenient to record but not to process. Now we live with this.
				outArray[:, 0, 1] = rawArr[:, 0]
				outArray[:, 1, 1] = rawArr[:, 1]
				outArray[:, 0, 0] = rawArr[:, 2]
				outArray[:, 1, 0] = rawArr[:, 3]
				outData[currLabel] = outArray

				print(f"\n\n\nLabel:{currLabel}")
				print(rawArr)
				print(f"   ->")
				print(outArray)
			currLabel = None
			currData = []
			continue
		
		if currLabel == None:
			currLabel = fooType(foo[:-1])
			continue
			# print(f"label:{currLabel}")

		if currLabel != None:
			currData.append([int(char) for char in foo[:-1]])

	return outData

# Load rotations
rotations = loadTxt('constants/block_rotations.txt', int)
vertices = loadTxt('constants/block_vertices.txt', str)

# for foo in rotations: print(f"{foo}:{rotations[foo]}")

# for foo in vertices: print(f"{foo}:{vertices[foo]}")

outDict = {
	'rotations':rotations,
	'vertices':vertices,
}


pkl.dump(outDict, open('constants/constants.pkl', 'wb'))