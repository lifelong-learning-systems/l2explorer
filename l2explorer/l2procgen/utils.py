"""
Copyright © 2021 The Johns Hopkins University Applied Physics Laboratory LLC
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import numpy as np
import matplotlib
import matplotlib.patches as mpl_patches
import matplotlib.path as mpl_path
import matplotlib.pyplot as plt
import json
from typing import List, Set, Dict, Tuple, Optional

#
# To change the seed, use
#  l2random.seed.(N), where N is an integer.
l2random = np.random.RandomState()


class OccupancyGrid():
    def __init__(self, xlim, ylim, resolution):
        (xlow, xhigh) = xlim
        (ylow, yhigh) = ylim
        self.xlims = (xlow, xhigh+resolution)
        self.ylims = (ylow, yhigh+resolution)
        self.resolution = resolution
        # xticks and yticks are in world coordinates
        self.xticks = np.arange(self.xlims[0], self.xlims[1], resolution)
        self.yticks = np.arange(self.ylims[0], self.ylims[1], resolution)
        # this is a row-major representation. self.grid[0,:] is the first row
        # which is notionally line with x=0.
        self._grid = np.zeros((len(self.xticks), len(self.yticks)), dtype=bool)
            

    def world2grid(self, x,y):
        # TODO: what if x is below or above the valid range
        # the astype allows the code to vectorize efficienty, when 
        # x and y are arrays.
         xg= ((x-self.xticks[0])/self.resolution).astype(np.int32)
         yg= ((y-self.yticks[0])/self.resolution).astype(np.int32)
         return (xg,yg)
    
    def set_occupied(self, x, y, val=True):
        # works if x and y are arrays
        xg,yg = self.world2grid(x,y)
        self._grid[xg,yg] = val
    
    def is_inbounds(self, x, y):
        x_inbounds = ~np.logical_or(x < self.xlims[0], x > self.xlims[1])
        y_inbounds = ~np.logical_or(y < self.ylims[0], y > self.ylims[1])
        return np.logical_and(x_inbounds, y_inbounds)

    def is_occupied(self, x, y):
        # works if x and y are arrays (returns an array of values)
        xg,yg = self.world2grid(x,y)
        return self._grid[xg,yg]
    
    def set_occupied_poly(self, poly, val=True):
        # set the polygon to "occupied"
        # TODO: if the polygon boundary falls within tick points, then
        # it is possible to have a partially-filled cell that is 
        # marked as empty
        xx,yy = np.meshgrid(self.xticks, self.yticks)
        # note that mesh_pts are in world coordinates
        mesh_pts = np.vstack([np.ravel(xx), np.ravel(yy)]).T            
        # check both at mesh points and meshpoints + resolution
        # to take care of scenarios where polygon boundary falls
        # between mesh points
        contained = np.logical_or(
                        poly.inside_poly(mesh_pts), 
                        poly.inside_poly(mesh_pts+self.resolution))
        mesh_pts = mesh_pts[contained]
        self.set_occupied(mesh_pts[:,0], mesh_pts[:,1])

    def show(self, ax):
        # Transponse before plotting. the Grid has a row-major representation
        # with axis 0 being "x", and axis 1 being "y". If it is plotted as-is
        # x increases along the vertical dimension. Hence, transpose 
        # befefore plotting.
        ax.imshow(self._grid.T, origin="lower")


class MyPolygon():
    def __init__(self, vertices):
        # Sample usage:
        #   vertices = np.array([(20,50),(50,100),(200,100),(200,20)]) 
        #  poly = MyPolygon(vertices)
        self.path = mpl_path.Path(vertices)
        self.vertices = vertices

    def tolist(self):
        return self.vertices.tolist()

    def plot(self, ax:matplotlib.axes):
        # fig = plt.figure()
        patch = mpl_patches.PathPatch(self.path, fill=True, facecolor="blue", alpha=0.1, lw=1)
        ax.add_patch(patch)

    def inside_poly(self, pts):
        contained = np.array( self.path.contains_points(pts) )
        return contained


def plot_locations(obj_locs, occgrid:OccupancyGrid, polygons:List[MyPolygon]):
    fig1 = plt.figure()
    occgrid.show(plt.axes(label="occgrid"))

    fig2 = plt.figure()
    ax2 = plt.axes()
    for poly in polygons:
        poly.plot(ax=ax2)
    for (obj_type, locs) in obj_locs.items():
        print("obj_type={0}, num pts={1}".format(obj_type, len(locs)))
        ax2.scatter(locs[:,0], locs[:,1])
    plt.show()


def write_l2explorer_json(json_info:dict, filename="params.json"):
    with open(filename, "w") as file:
        json.dump(json_info, file, indent=4)
    print("saved to ", filename)            
