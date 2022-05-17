[Outline](Outline.md) -> [Channels](Channels.md) -> Reset Channel

# Reset Channel

- [Example Object Create messages](#Example-Object-Create-messages)
- [Example Reset message](#Example-Reset-message)
- [Object Defaults](#Object-Defaults)
- [Description of fields](#Description-of-fields)

## Example Object Create messages

This message will create a new tree at the given coordinates

```json
{
  "token": "584c18df-2461-4121-95b0-3f0c7d1ae267",
  "msg_time": "2020-07-29T15:41:39.8418369Z",
  "action": "object_create",
  "unique_name": "thing",
  "payload": {
    "class": "tree",
    "model": "49",
    "coordinates": [33.4, 56.6],
    "color": [0.0, 0.0, 1.0],
    "motion_model": "stationary"
  }
}
```

This message will dynamically create a red target at the given coordinates, which will provide a single reward as the agent gets close, but get destroyed on contact with the agent

```json
{
  "token": "584c18df-2461-4121-95b0-3f0c7d1ae268",
  "msg_time": "2020-07-29T15:41:39.8418379Z",
  "action": "object_create",
  "unique_name": "target_123546",
  "payload": {
    "model": "1",
    "class": "geometric",
    "coordinates": [12.4, 10],
    "color": [1.0, 0.0, 0.0],
    "motion_model": "stationary",
    "destroy_stimulus": ["AgentCollide"],
    "reward_once_stimulus": ["AgentInRange"],
    "range_stimulus_distance": 2,
    "reward": 0.25
  }
}
```

## Example Reset message

The environment is ultimately controlled by a CustomResetParameters object sent every reset() which has one string field. This field is a flattened JSON which specifies object locations, agent status, etc.

This is an example of a reset message:

```json
{
  "token": "584c18df-2461-4121-95b0-3f0c7d1ae266",
  "msg_time": "2020-07-29T15:41:39.8418368Z",
  "action": "reset_environment",
  "payload": {
    "game_mode": "learn",
    "max_steps": 3000,
    "environment_params": {
      "bounding_wall_color": [1.0, 0.75, 1.0],
      "light_intensity": 2.3,
      "predefined_map": 0,
      "map_size": [100, 100]
    },
    "agent_params": {
      "action_model": "byvelocity",
      "agent_height": 1.0,
      "agent_width": 1.0,
      "max_linear_speed": 10.0,
      "max_angular_speed": 90.0,
      "observation_size": 128,
      "coordinates": [34.5, 45.6],
      "heading": 10.0
    },
    "image_params": {
      "zoom": 5,
      "yaw_subdivisions": 24,
      "vertical_subdivisions": 5
    },
    "objects": [
      {
        "class": "tree",
        "model": "49",
        "coordinates": [34.4, 56.6],
        "color": [1.0, 1.0, 1.0],
        "motion_model": "stationary",
        "reward": 1.0
      },
      {
        "model": "4",
        "class": "Chair",
        "coordinates": [45.4, 54.5],
        "color": [0.1, 0.4, 1.0],
        "motion_model": "stationary",
        "reward": 150.0,
        "reward_stimulus": ["AgentInteract"],
        "destroy_stimulus": ["AgentInteract"],
        "interaction_distance": 0.0
      },
      {
        "model": "1",
        "class": "geometric",
        "coordinates": [12.4, 4.5],
        "color": [1.0, 0.0, 0.0],
        "motion_model": "stationary",
        "reward": -35.0,
        "reward_stimulus": ["AgentCollide"]
      },
      {
        "model": "3",
        "class": "building",
        "coordinates": [12.4, 4.5],
        "color": [1.0, 1.0, 1.0],
        "motion_model": "stationary",
        "reward": 0.0,
        "collectible": false,
        "reward_on": "none",
        "interaction_distance": 0.0
      }
    ]
  }
}
```

## Object Defaults

When an object is defined with incomplete information, e.g. an entry is missing or has an invalid value type, the environment internally defaults to the following values for any missing fields. Note that 'class' defaults to an empty string; if no class is specified, the object will be skipped.

```json
{
  "model": "1",
  "class": "",
  "coordinates": [0.0, 0.0],
  "color": [0.0, 0.0, 0.0],
  "motion_model": "stationary",
  "reward": 0.0,
  "range_stimulus_distance": 0,
  "reward_stimulus": [],
  "reward_once_stimulus": [],
  "destroy_stimulus": []
}
```

## Description of fields

Note that all string fields are case-insensitive.

- `game_mode` : choice of "learn", "collect_images" : whether the environment is being used to train an RL agent or to collect images. In release v0.2.6, only "learn" is allowed.
- `max_steps` : int range `[0, inf)` : How many steps until the environment resets. A value of 0 indicates that it runs indefinitely.
- `environment_params` : affects non-object things
  - `bounding_wall_color` : float[3] range `[0,1]` : defines the RGB color of the walls around the map
  - `lightIntensity` : float range `[0,inf)` : how bright the sunlight is.
  - `predefined_map` : int `[0, 4]` : Which predefined map to load, 1 through 4. A value of 0 loads an empty map; if a map is loaded, it will override the value of map_size to suit the chosen map.
    - `map_size` : int[2] range `[0,300]` : defines placement of the boundary walls around the map. If predefined_map is not 0, this field has no effect.
- `agent_params` : fields which affect the agent's movement and interactions.
  - `action_model` : choice of "byvelocity", "bywaypoint", "onrails", "none" : Describes how the agent's inputs are translated into movement and interactions.
  - `agent_height` : float `(-inf,inf)` : How high off the ground the agent's FPV camera is.
  - `agent_width` : float `(0, inf)` : How large the agent's collider is.
    - `max_linear_speed` : float `[0, inf)` : highest m/s of forward/backward movement the agent is allowed to achieve.
    - `max_angular_speed` : float `[0, inf)` : highest degrees/second turning rate the agent is allowed to achieve.
    - `observation_size` : int `[1, inf)` : How many pixels wide & tall the agent's visual observation will be.
    - `coordinates` : float[2] range `[-300, 300]` : Where the agent spawns at the start of the episode.
    - `heading` : float range `[0, 360]` : Agent heading, in degrees
- `image_params` : Details of image collection mode; not supported in release v0.2.6. Any values set in these fields will be ignored.
- `objects` : a list of props and buildings to spawn. Can be any length; an empty list will cause nothing to be placed.
  - `model` : int, see 'available models' : Which object within the class to spawn
  - `class` : choice of strings, see 'available models' : Which class of objects to spawn
  - `coordinates` : float[2] range `[-300, 300]` : Where the object will be placed.
  - `color` : float[3] range `[0,1]` : The main color of the object. May or may not apply to every texture on the model.
  - `motion_model` : choice of "stationary", "predator", "prey", "random_waypoint" : Which motion script to attach to the object. For release v0.2.6, only "stationary" is supported.
  - `reward` : float `(-inf, inf)` : How much reward to give the agent for interacting with this object. Rewards can be repeated under certain circumstances - see 'Object interactions' for more information.
  - `range_stimulus_distance` : float `(0, inf)` : At what distance is `AgentInRange` triggered
  - `reward_stimulus`: string[] : What stimuli will cause this object to provide its reward to the agent? This is for recurring rewards / penalties
  - `reward_once_stimulus`: string[] : What stimuli will cause this object to provide its reward to the agent? This is for one-shot rewards / penalties (the reward will be set to zero after the first time it is provided to the agent)
  - `destroy_stimulus`: string[] : What stimuli will cause this object to be destroyed?

## Object Interaction Options, used for Reward Stimulus 

- AgentCollide : Triggers when the agent collides with the object
- AgentInteract : Triggers when the agent explicitly attempts to interact with the object while it is in the agent's interaction volume
- AgentInRange : Triggers when the agent is within this range (centroid to centroid in 3D space, so the value should be larger than the radius of the object + the radius of the agent)
