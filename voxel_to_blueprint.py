import json
import numpy as np
from stl import mesh
from matplotlib import pyplot as plt
import pickle as pkl
from matplotlib import pyplot as plt

MAKE_SCATTER_PLOT = False

FILE_NAME = 'hull'

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

outputPoints = pkl.load(open(f"processing/{FILE_NAME}_vox.pkl", 'rb'))

halfGridShape = outputPoints.shape
mirrorPts = np.zeros((halfGridShape[0]*2, halfGridShape[1], halfGridShape[2]), dtype=np.int16)

setPoints = np.where(outputPoints == 1)[0]
setPoints[0] += shape[0]
mirrorPts[setPoints] = 1





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

if MAKE_SCATTER_PLOT:
	setPoints = np.where(outputPoints > 0)
	print(setPoints)
	ax = plt.figure().add_subplot(projection='3d')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	ax.scatter(*setPoints, color='blue')

	set_axes_equal(ax)
	plt.show()

	# print(path)
	exit()



shape = outputPoints.shape
mirrorPts = np.zeros((shape[0]*2, shape[1], shape[2]), dtype=np.int16)

setPoints = np.where(outputPoints == 1)[0]
setPoints[0] += shape[0]
mirrorPts[setPoints] = 1

print(f"outputPoints:{np.sum(outputPoints)}/{outputPoints.shape[0]*outputPoints.shape[1]*outputPoints.shape[2]}")
print(f"mirrorPts:{np.sum(mirrorPts)}/{mirrorPts.shape[0]*mirrorPts.shape[1]*mirrorPts.shape[2]}")

for fooPt in np.swapaxes(np.array(np.where(mirrorPts == 1)), 1, 0):
	blockIDS.append(565)
	# blockPlacements.append(f"{xx},{yy},{zz}")
	blockPlacements.append(f"{fooPt[1]},{fooPt[2]},{fooPt[0]}")
	blockRotations.append(0)
	blockColors.append(0)

blueprint['Blueprint']['BlockIds'] = blockIDS
blueprint['Blueprint']['BLP'] = blockPlacements
blueprint['Blueprint']['BLR'] = blockRotations
blueprint['Blueprint']['BCI'] = blockColors
json.dump(blueprint, open('output/GENERATED_BLUEPRINT.blueprint', 'w'))

