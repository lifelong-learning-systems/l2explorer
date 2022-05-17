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
Example of procedural generation with customization of the templates
"""

exmap = L2ExplorerMap(map_id=1)

# specify objects and relationships

available_classes = templates.get_available_object_classes()
print("Available object classes:", available_classes)

object_generation_sequence = ["tree", "shrub", "rock", "barrel",
                              "mushroom", "tent", "building", "streetsign", "roadblock", "fence", "car"]

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
        "co-occurrence": constant(10),
        "spatial-dist": uniform_box_c(xlims=xlim, ylims=ylim)},
    ("shrub", None): {
        "co-occurrence": constant(10),
        "spatial-dist": uniform_box_c(xlims=xlim, ylims=ylim)},
    ("rock", None): {
        "co-occurrence": constant(10),
        "spatial-dist": uniform_box_c(xlims=xlim, ylims=ylim)},
    ("barrel", None): {
        "co-occurrence": constant(10),
        "spatial-dist": uniform_box_c(xlims=xlim, ylims=ylim)},
    ("mushroom", None): {
        "co-occurrence": constant(10),
        "spatial-dist": uniform_box_c(xlims=xlim, ylims=ylim)},
    ("tent", None): {
        "co-occurrence": constant(5),
        "spatial-dist": uniform_box_c(xlims=xlim, ylims=ylim)},
    ("building", None): {
        "co-occurrence": constant(5),
        "spatial-dist": uniform_box_c(xlims=xlim, ylims=ylim)},

    ("fence", "building"): {
        "co-occurrence": binomial(n=2, p=0.9),
        "spatial-dist": annulus_c(rmin=2, rmax=5)},
}


procgen.generate_bare_objects_in_map(exmap, object_generation_sequence, conditional_distributions)

agent_params = templates.agent_template
agent_params.update({
    "max_linear_speed": 15.0,
    "max_angular_speed": 85.0,
    "observation_size": 84,
})

env_params = templates.environment_template
env_params.update({
    "bounding_wall_color": [0, 100, 255],
    "light_intensity": 3.0,
    "predefined_map": '1',
})

image_params = templates.image_template
image_params.update({
    "yaw_subdivisions": 4,
    "vertical_subdivisions": 22
})

# customize the object templates
object_templates = templates.object_templates
object_templates['rock'] = {
    'class': 'rock',
    'color': choice([[0, 1, 0], [1, 1, 0]]),
    'destroy_stimulus': [
        "AgentCollide"
    ],
    'reward_once_stimulus': [
        "AgentCollide"
    ],
    'reward': perturb(10, limits=(9, 11), noise=0.1),
    'motion_model': "stationary",
    'model': choice(['11', '22', '33', '44']),
}

full_objects = procgen.make_full_objects(
    exmap, object_templates=object_templates)

json_info = templates.make_toplevel_json_object(full_objects,
                                                agent_params=agent_params,
                                                env_params=env_params,
                                                image_params=image_params)

utils.write_l2explorer_json(json_info, filename="resetparams2.json")

exmap.summary()
exmap.plot()
