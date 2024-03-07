import json
import numpy as np
from matplotlib import pyplot as plt
import pickle as pkl
import os
import pyvista as pv

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

FILE_NAME = 'hull'
# FILE_NAME = 'cube'
# FILE_NAME = 'ball'
# FILE_NAME = '3DBenchy'


surface = pv.PolyData(f'input/{FILE_NAME}.stl')
voxels = pv.voxelize(surface, density=1)

voxPoints = voxels.points
# np.swapaxes(voxels.points, 0, 1)



# Normalize
for fooAx in range(3): voxPoints[:, fooAx] -= np.min(voxPoints[:, fooAx])
# p = pv.Plotter()
# p.add_mesh(voxels, color=True, show_edges=True, opacity=0.5)
# p.add_mesh(surface, color="lightblue", opacity=0.5)
# p.show()

voxPoints = np.array(voxPoints, dtype=np.uint8)

outputArrShape = np.max(voxPoints, axis=0) + 1

print(f"outputArrShape:{outputArrShape}")

outputPoints = np.zeros(outputArrShape, dtype=np.int16)

outputPoints[*np.swapaxes(voxPoints, 0, 1)] = 1

pkl.dump(outputPoints, open(f"processing/{FILE_NAME}_vox.pkl", 'wb'))

exit()

# Using an existing stl file:
hull_mesh = mesh.Mesh.from_file(f'input/{FILE_NAME}.stl')

xyz = np.concatenate([hull_mesh.points[:, 3*ii:3*(ii+1)] for ii in range(3)])

print(hull_mesh.points.shape)
print(xyz.shape)

wallThickness = 4.5
sizeMargin = 10

xyz[:, 0] += sizeMargin - np.floor(np.min(xyz[:, 0]))
xyz[:, 1] -= (np.max(xyz[:, 1]) + np.min(xyz[:, 1]))/2
xyz[:, 2] += sizeMargin - np.floor(np.min(xyz[:, 2]))


hull_mesh.points[:, 0::3] += sizeMargin - np.floor(np.min(hull_mesh.points[:, 0::3]))
hull_mesh.points[:, 1::3] -= (np.max(hull_mesh.points[:, 1::3]) + np.min(hull_mesh.points[:, 1::3]))/2
hull_mesh.points[:, 2::3] += sizeMargin - np.floor(np.min(hull_mesh.points[:, 2::3]))


print(f"X:({np.min(xyz[:, 0])}, {np.max(xyz[:, 0])})")
print(f"Y:({np.min(xyz[:, 1])}, {np.max(xyz[:, 1])})")
print(f"Z:({np.min(xyz[:, 2])}, {np.max(xyz[:, 2])})")

# Need to modify (in ["Blueprint"])
# BlockIDS: What block is being place
# BLP: Placement of block (list of strings for some reason)
# BLR: Block rotation
# BCI: Block color I think

blockIDS = []
blockPlacements = []
blockRotations = []
blockColors = []

for fooPt in np.swapaxes(np.array(np.where(mirrorPts == 1)), 1, 0):
	blockIDS.append(565)
	# blockPlacements.append(f"{xx},{yy},{zz}")
	blockPlacements.append(f"{fooPt[1]},{fooPt[2]},{fooPt[0]}")
	blockRotations.append(0)
	blockColors.append(0)
	outPts.append(fooPt)



if not os.path.isdir('output'):
	os.makedirs('output')
	
if not os.path.isdir('processing'):
	os.makedirs('processing')


blueprint['Blueprint']['BlockIDS'] = blockIDS
blueprint['Blueprint']['BLP'] = blockPlacements
blueprint['Blueprint']['BLR'] = blockRotations
blueprint['Blueprint']['BCI'] = blockColors

json.dump(blueprint, open(f"output/{FILE_NAME}_cubes.blueprint", 'w'))
