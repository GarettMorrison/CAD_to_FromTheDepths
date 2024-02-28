#! /usr/bin/env python

from solid2.extensions.bosl2 import circle, cuboid, sphere, cylinder, \
									heightfield, diff, tag, attach, \
									TOP, BOTTOM, CTR, metric_screws, rect, glued_circles, \
									chain_hull, conv_hull, hull, cube, union, trapezoid, teardrop, skin, sweep

from solid2.extensions.bosl2.turtle3d import turtle3d

from solid2.core import linear_extrude

import numpy as np
from scipy.interpolate import splprep, splev
from scipy.spatial.distance import cdist
from random import random
from copy import deepcopy
import pickle as pkl
import sys
import os


roundRad = 4


hullObjSet = []
hullObjSet.append(cylinder(10, 10, 16))
hullObjSet.append(cylinder(10, 10, 16).translate([10,0,0]))

hullVol = conv_hull()(*hullObjSet)
hullVol.save_as_scad(f"generated_hull.scad")