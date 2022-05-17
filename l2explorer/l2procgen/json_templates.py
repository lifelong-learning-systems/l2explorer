import numpy as np
from .distributions import *

def get_available_object_classes():
    return list(object_templates.keys())

global_template = {
		"model": "1",
		"class": "",
		"coordinates": [0.0, 0.0],
		"color": [0.0, 0.0, 0.0],
		"motion_model": "stationary",
		"reward": 0.0,
		"destroy_stimulus" : [],
		"reward_once_stimulus" : [],
		"range_stimulus_distance" : 0.0
}

# templates for individual object classes.
# Note that wew can define new object classes (e.g., "green_tree") with a customized set of parameters
object_templates = {
    'agent':{
        'class': 'agent',
        'model': 'agent',
    },
    'tree': {
        'class': 'tree',
        'color': perturb([0.0, 0.5, 0.5], noise=0.2),
        'reward': 1.0,
        'motion_model': "stationary",
        'model': choice([str(x) for x in range(1,50)]),
    },
    'geometric': {
        'class': 'geometric',
        'color': perturb([0.0, 0.5, 0.5], noise=0.2),
        'reward': 1.0,
        'motion_model': "stationary",
        'model': choice(['1', '2', '3']),
    },
    'nature': {
        'class': choice(['rock', 'shrub', 'tree']), #autogenerate nature background objects
        'model': choice([str(x) for x in range(1,12)]) #use the lowest number of classes for rock so this is consistent across them
    },
    'shrub':{
        'class': 'nature',
        'model': 'shrub',
    },
    'bag':{
        'class': 'bag',
        'model': choice([str(x) for x in range(1,7)]),
    },
    'barrel':{
        'class': 'barrel',
        'model': choice([str(x) for x in range(1,6)]),
    },
    'bench':{
        'class': 'bench',
        'model': choice([str(x) for x in range(1,4)]),
    },
    'building':{
        'class': 'building',
        'model': choice([str(x) for x in range(1,3)]),
    },
    'castleruin':{
        'class': 'castleruin',
        'model': choice([str(x) for x in range(1,8)]),
    },
    'chair':{
        'class': 'chair',
        'model': choice([str(x) for x in range(1,3)]),
    },
    'mushroom':{
        'class': 'mushroom',
        'model': choice([str(x) for x in range(1,7)])
    },
    'pot':{
        'class': 'pot',
        'model': choice([str(x) for x in range(1,5)])
    },
    'rock':{
        'class': 'rock',
        'model': choice([str(x) for x in range(1,19)])
    },
    'shelf':{
        'class': 'shelf',
        'model': choice([str(x) for x in range(1,2)])
    },
    'shrub':{
        'class': 'shrub',
        'model': choice([str(x) for x in range(1,12)])
    },
    'tent':{
        'class': 'tent',
        'model': choice([str(x) for x in range(1,4)])
    },
    'table':{
        'class': 'table',
        'model': choice([str(x) for x in range(1,4)])
    },
    'mushroom':{
        'class': 'mushroom',
        'model': choice([str(x) for x in range(1,7)])
    },
    'fence':{
        'class': 'fence',
        'model': choice([str(x) for x in range(1,32)])
    }

}



agent_template = {
    "action_model": "byvelocity",
    "agent_height" : 1.0,
    "agent_width" : 1.0,
    "max_linear_speed": 10.0,
    "max_angular_speed" : 90.0,
    "observation_size": 128,
    "coordinates": [34.5, 45.6],
    "heading": 10.0
	}

image_template = {
    "zoom" : 5,
    "yaw_subdivisions" : 5,
    "vertical_subdivisions" : 24
}

environment_template = {
    "bounding_wall_color": [0, 0, 255],
    "light_intensity": 3.0,
    "predefined_map" : '1',
    "map_size": [100, 100]
}

def make_toplevel_json_object(objects, max_steps=3000, env_params=environment_template,
                                agent_params=agent_template, image_params=image_template):
    return  {
        "game_mode": "learn",
        "max_steps": max_steps,
        "environment_params": env_params,
        "agent_params": agent_params,
        "image_params" : image_params,
        "objects": objects
    }
