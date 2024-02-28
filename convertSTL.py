import json
import numpy as np
from stl import mesh
from matplotlib import pyplot as plt


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



# Using an existing stl file:
hull_mesh = mesh.Mesh.from_file('squareHull.stl')
# hull_mesh = mesh.Mesh.from_file('hull.stl')
# hull_mesh = mesh.Mesh.from_file('cube.stl')
print(f"\n\n\n\n")
# print(.shape)
xyz = np.concatenate([hull_mesh.points[:, 3*ii:3*(ii+1)] for ii in range(3)])

print(hull_mesh.points.shape)
print(xyz.shape)

wallThickness = 4.5
sizeMargin = 10

xyz[:, 0] += sizeMargin - np.floor(np.min(xyz[:, 0]))
xyz[:, 1] += sizeMargin - np.floor(np.min(xyz[:, 1]))
xyz[:, 2] += sizeMargin - np.floor(np.min(xyz[:, 2]))


hull_mesh.points[:, 0::3] += sizeMargin - np.floor(np.min(hull_mesh.points[:, 0::3]))
hull_mesh.points[:, 1::3] += sizeMargin - np.floor(np.min(hull_mesh.points[:, 1::3]))
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

outputPoints = np.zeros((int(np.ceil(np.max(xyz[:, 0])) + sizeMargin), int(np.ceil(np.max(xyz[:, 1])) + sizeMargin), int(np.ceil(np.max(xyz[:, 2])) + sizeMargin)), dtype=np.int16)


fooPt_set = []
closestPt_set = []


ptInd = -1
for fooPt in hull_mesh.points:
	ptInd += 1 
	p0 = fooPt[:3]
	p1 = fooPt[3:6]
	p2 = fooPt[6:9]
	x0, y0, z0 = p0
	x1, y1, z1 = p1
	x2, y2, z2 = p2
	

	# ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
	# vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]
	# u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]
	# point  = np.array(p0)
	# normal = np.array(u_cross_v)
	u = p1 - p0
	v = p2 - p0

	normal = np.cross(u, v)	
	normalMag = np.sqrt(normal.dot(normal))
	normalVect = normal/normalMag
	D = -np.sum(normalVect * p0)
	print(f"D:{D}     norm:{normalVect}")

	pointRange = np.array([[int(np.min(fooPt[ii::3]) - wallThickness), int(np.max(fooPt[ii::3]) + wallThickness)] for ii in range(3)])

	

	# for fooPt in [p0, p1, p2]:
	# 	normPt = np.array([fooPt, normalVect + fooPt])
	# 	ax.plot(normPt[:, 0], normPt[:, 1], normPt[:, 2], color='red')

	# continue

		
	# ax = plt.figure().add_subplot(projection='3d')
	# ax.set_xlabel('X')
	# ax.set_ylabel('Y')
	# ax.set_zlabel('Z')
	
	# # ax.scatter(*np.swapaxes([p0, p1, p2], 0, 1), color='blue')
	
	# ax.scatter(*p0, color='blue')
	# ax.scatter(*p1, color='green')
	# ax.scatter(*p2, color='black')

	areaABC = normalMag/2

	for fooPt in np.swapaxes(np.array(np.where(outputPoints == 0)), 1, 0):
		# Only consider points within bounding box
		doContinue = False
		for ii in range(3):
			if fooPt[ii] < pointRange[ii, 0] or fooPt[ii] > pointRange[ii, 1]:
				doContinue = True
				break
		if doContinue: 
			continue
		
		# dist = (normal@(testPt-p0))/(np.sqrt(np.sum(np.square(normal))))
		# if abs(dist) > 2: continue

		# Get distance to plane
		# planeDist = ( np.sum(normalVect*fooPt) + D) / normalMag
		w = fooPt - p0

		planeDist = np.dot(fooPt - p0, normalVect)
		
		# print(planeDist)

		if planeDist < -wallThickness or planeDist > 0:
			# print(f"planeDist:{planeDist}")
			continue

		closestPt = fooPt - planeDist*normalVect
		
		# # Check that closest point is inside triangle
		# alpha = np.sqrt(np.sum(np.square(np.cross((p1 - closestPt), (p2 - closestPt))))) / normalMag
		# beta = np.sqrt(np.sum(np.square(np.cross((p2 - closestPt), (p0 - closestPt))))) / normalMag
		# theta = 1 - alpha - beta

		alpha = np.cross(u, w).dot(normal) / normal.dot(normal)
		beta = np.cross(w, v).dot(normal) / normal.dot(normal)
		theta = 1 - alpha - beta

		# print(f"alpha:{alpha}")
		# print(f"beta:{beta}")
		# print(f"theta:{theta}")

		if alpha >= 1 or alpha <= 0: continue
		if beta >= 1 or beta <= 0: continue
		if theta >= 1 or theta <= 0: continue

		roundPt = np.array(np.round(closestPt), dtype=np.int32)

		# if outputPoints[fooPt[0], fooPt[1], fooPt[2]] == 1:
		# 	continue

		outputPoints[fooPt[0], fooPt[1], fooPt[2]] = 1
		# print(np.swapaxes([closestPt, fooPt], 0 ,1))

		fooPt_set.append(fooPt)
		closestPt_set.append(closestPt)

	# 	# ax.plot(*np.swapaxes([closestPt, fooPt], 0 ,1), color='blue')
	# 	# ax.scatter(*fooPt, color='orange')
	# 	# ax.scatter(*closestPt, color='red')
		
	# ax.scatter(*np.swapaxes(fooPt_set, 0, 1), color='orange')
	# ax.scatter(*np.swapaxes(closestPt_set, 0, 1), color='red')
	# plt.show()
		
# plt.show()
# exit(0)

# # showPts = np.swapaxes(np.array(np.where(outputPoints == 1)), 0, 1)
# showPts = np.array(np.where(outputPoints == 1))
# print(showPts)
# ax.scatter(*showPts)
# print("Showing!")
# plt.show()
# exit()








outPts = []

for fooPt in np.swapaxes(np.array(np.where(outputPoints == 1)), 1, 0):
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

ax = plt.figure().add_subplot(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.scatter(*np.swapaxes(closestPt_set, 0, 1), color='red')
ax.scatter(*np.swapaxes(fooPt_set, 0, 1), color='orange')
plt.show()
