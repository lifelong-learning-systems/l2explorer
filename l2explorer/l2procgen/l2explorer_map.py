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
from . import predefined_maps as pmaps
from . import utils
import matplotlib.pyplot as plt

class L2ExplorerMap(object):
    def __init__(self, map_id, cell_size=2):
        self.map_id = map_id
        (polygon_specs, xlim, ylim) = pmaps.get_map(map_id)
        self.xlim = tuple(xlim)
        self.ylim = tuple(ylim)
        self.occgrid = utils.OccupancyGrid(xlim=xlim, ylim=ylim, resolution=cell_size)
        self.polygons = []
        for poly_vertices in polygon_specs:
            poly = utils.MyPolygon(vertices=poly_vertices)
            self.occgrid.set_occupied_poly(poly)
            self.polygons.append(poly)
        self.obj_locs = {None: np.array([[0,0]])}


    def summary(self):
        print("L2ExplorerMap:")
        print(" id = ", self.map_id)
        print(" xlimits = {0}, ylimits ={1}".format(self.xlim, self.ylim))
        print(" polygons = ", len(self.polygons))
        print(" objects:")
        for (obj_type, locs) in self.obj_locs.items():
            print("    {0} x {1}".format(obj_type, len(locs)))


    def plot(self, to_show=('map')):
        if 'grid' in to_show:
            fig1 = plt.figure()
            self.occgrid.show(plt.axes(label="occgrid"))
        if 'map' in to_show:
            fig2 = plt.figure()
            ax2 = plt.axes()
            ax2.set_xlim(*self.xlim)
            ax2.set_ylim(*self.ylim)
            for poly in self.polygons:
                poly.plot(ax=ax2)
            plots = {}
            for (obj_type, locs) in self.obj_locs.items():
                if obj_type is not None:
                    plots[obj_type] = ax2.scatter(locs[:,0], locs[:,1])
            ax2.legend(list(plots.values()), list(plots.keys()), loc='upper right')
        plt.show()


    def add_objects(self, obj_class:str, locations:np.ndarray):
        if obj_class in self.obj_locs:
            self.obj_locs[obj_class] = np.append(self.obj_locs[obj_class], locations, axis=0)
        else:
            self.obj_locs[obj_class] = locations
        print("Adding {0} points for '{1}'".format(len(locations), obj_class))

    def get_objects_by_class(self, obj_class:str):
        return self.obj_locs.get(obj_class, None)

    def get_object_classes(self):
        lst = list(self.obj_locs.keys())        
        lst.remove(None)  # remove the 'None' key
        return lst

