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

import matplotlib
import matplotlib.patches as mpl_patches
import matplotlib.path as mpl_path
import matplotlib.pyplot as plt
import numpy as np
import pdb
import pprint
import json
import argparse
import copy

import l2explorer.l2procgen.json_templates as templates


"""
Joint Probabilites factor as below. Consequently, we can start with "x", then 
calculate P(y), then (having y&x), calculate z and so on. 
P(y & x) = P(y | x) * P(x)
P(z & y & x) = P(z | y & x) * P(y & x) = P(z | y & x) * P(y | x) * P(x)

Note: 
For a pair of objects (y and x), need 
1) An ordering of the objects (e.g., first x, then y), and
2) conditional probabilities of y given x. This consists of two things:
   a) co-occurrence prob (how often does Y co-occur with X)
   b) spatial distribution (if Y does occur, where does it occur relative to x)

For 2a (co-occurrence): probability p, and n max possible objects. Binomial distribution
      result: K objects drawn from Binomial(n,p)

For 2b (spatial distribution): P(location of an instance of y | location of x)
      can specify a toroid distribution. Pick radius r as Unif(rmin,rmax), and
      angle theta as unif(0,2*pi).

We should ensure that none of the objects "sit on top" of each other, i.e.,
there is always a minimum distance D between objects. Basically, whenever we sample
for a spatial location, we do two checks
  * is it at least D away from points already present, and
  * is it inside any forbidden areas?
if yes, resample.
"""
import numpy as np
from .utils import *
from .utils import OccupancyGrid, MyPolygon


def generate_bare_objects_in_map(exmap, object_gen_sequence, conditional_distributions):
    # the pairs in conditional_distributions should be processed in a specific
    # order. For  object_gen_sequence=[a,b,c,d], all pairs (y,x) with x=a 
    # should be processed first; then all pairs with x=b, and so on.
    # The following logic generates this ordered sequence of pairs and 
    # filters it by the pairs that are actually present in conditional_distributions

    if object_gen_sequence[0] is not None:
        object_gen_sequence.insert(0, None)

    object_pairs = []
    num_objs = len(object_gen_sequence)
    for i in range(num_objs):
        for j in range(i+1, num_objs):
            pair = (object_gen_sequence[j], object_gen_sequence[i])
            if pair in conditional_distributions:
                object_pairs.append(pair)

    occgrid = exmap.occgrid
    print("object pairs:", object_pairs)
    # now process the pairs in order, generating points for each.
    for pair in object_pairs:
        (y, given_x) = pair
        locs_y = np.empty((0,2))

        # sample all the y points, given a specific x
        locations_x = exmap.get_objects_by_class(given_x)
        for loc_givenx in locations_x:
            (cx,cy) = loc_givenx
            locs_y_givenx = np.empty((0,2))
            num_y = conditional_distributions[pair]["co-occurrence"]()
            for i in range(num_y):
                oversample = 4
                context = ((cx,cy),)
                pts = conditional_distributions[pair]["spatial-dist"](context, count=oversample)
                locs_y_givenx = np.append(locs_y_givenx, pts, axis=0)
                        
            if len(locs_y_givenx) == 0:
                continue
            
            # remove duplicated elements
            locs_y_givenx = np.unique(locs_y_givenx, axis=0)
            is_inbounds = occgrid.is_inbounds(locs_y_givenx[:,0], locs_y_givenx[:,1])
            locs_y_givenx = locs_y_givenx[is_inbounds]            
            # the OccGrid check enforces both rule 1 (minimum distance) and 
            # rule 2 (can't be inside a polygon), as the OccGrid includes the
            # polygon information as well.
            occupied = occgrid.is_occupied(locs_y_givenx[:,0], locs_y_givenx[:,1])
            locs_y_givenx = locs_y_givenx[~occupied]
            # shuffle and pick at most the first num_y points (if available)
            # if there are fewer and num_y points, all of them are selected
            l2random.shuffle(locs_y_givenx)
            locs_y_givenx = locs_y_givenx[:num_y]
            # add the newly-selected points to the occupancy grid
            occgrid.set_occupied(locs_y_givenx[:,0], locs_y_givenx[:,1])

            # add to list of points selected for loc_givenx
            locs_y = np.append(locs_y, locs_y_givenx, axis=0)
            
        exmap.add_objects(y, locs_y)




def make_full_objects(exmap, global_template=templates.global_template, object_templates=templates.object_templates):
    obj_classes = exmap.get_object_classes()
    objects = []
    for object_class in obj_classes:
        locs = exmap.get_objects_by_class(object_class)
        print("object_type:", object_class, "locations:", len(locs))
        obj_template = copy.deepcopy(global_template)
        obj_template.update(object_templates[object_class])
        callable_fields = [k for k in obj_template.keys() if callable(obj_template[k])]

        for loc in locs:
            context = (loc)
            obj = copy.deepcopy(obj_template)
            obj['coordinates'] = list(loc)
            for f in callable_fields:
                value = obj_template[f](context)
                if isinstance(value, np.ndarray):
                    obj[f] = list(value)
                else:
                    obj[f] = value
            if len(obj['color']) != 3:
                raise RuntimeError("oops")
            objects.append(obj)
    return objects


