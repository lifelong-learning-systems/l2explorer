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

import l2explorer
from l2explorer.l2procgen import json_templates as templates
from l2explorer.l2procgen import procedural_gen as procgen
from l2explorer.l2procgen import utils as utils
from l2explorer.l2procgen.distributions import *
from l2explorer.l2procgen.l2explorer_map import L2ExplorerMap

"""
Basic example of procedural generation
"""
exmap = L2ExplorerMap(map_id=2)

# specify objects and relationships

available_classes = templates.get_available_object_classes()
print("Available object classes:", available_classes)

object_generation_sequence = ["tree", "shrub", "rock"]

# (Y,X) indicates conditional distribution of Y, given X
# (Y,None) means conditional distribution of Y based on no priors 
# Each conditional distribution consists of two pieces of information
#    co-occurrence (N) = 
#            how many Y's to pick for each value of X. 
#            N could be a constant or chosen randomly (e.g., from a binomial distribution).
#    spatial-dist (P) =
#            For each Y, this specifies how to sample the spatial
#            coordinates of Y. This can be rotating through a fixed list of coordinates,
#           or sampling from a uniform 2D distribution, or an annulus, etc.
xlim, ylim = exmap.xlim, exmap.ylim
conditional_distributions = {
    ("tree", None): {
        "co-occurrence": constant(4),
        "spatial-dist": fixed_set([[-75, -75], [-75, 75], [75, -75], [75, 75]])},
    ("shrub", None): {
        "co-occurrence": constant(10),
        "spatial-dist": uniform_box_c(xlims=(-90, -30), ylims=(-10, 50))},
    ("rock", "tree"): {
        "co-occurrence": binomial(n=25, p=0.9),
        "spatial-dist": annulus_c(rmin=3, rmax=6)},
    ("rock", "shrub"): {
        "co-occurrence": binomial(n=10, p=0.9),
        "spatial-dist": annulus_c(rmin=2, rmax=7)}
}

procgen.generate_bare_objects_in_map(
    exmap, object_generation_sequence, conditional_distributions)
full_objects = procgen.make_full_objects(exmap)
json_info = templates.make_toplevel_json_object(full_objects)
utils.write_l2explorer_json(json_info, filename="resetparams3.json")

exmap.summary()
exmap.plot()
