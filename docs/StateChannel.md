[Overview](Outline.md) -> [Channels](Channels.md) -> State Channel

# State Channel

The state channel is for configuring and receiving state information.

## Get observers

Get a listing of observers supported in this version of the application

```json
{
  "token": "584c18df-2461-4121-95b0-3f0c7d1ae266", // generate new GUID for every message
  "msg_time": "2020-07-29T15:41:39.8418368Z", // Time of response
  "action": "get_observers"
}
```

## Observer listing

The response: A listing of available observers

```json
{
  "token": "d0d14d69-2f1f-42b3-ba11-36bfb22b323b",
  "req_token": "584c18df-2461-4121-95b0-3f0c7d1ae266",
  "msg_time": "2020-07-30T18:13:49.9532624Z",
  "action": "observer_list",
  "payload": {
    "state": ["agent_params", "environment_params", "objects", "game_mode"]
  }
}
```

## Set active observers

Tells the Unity application what items should be included in the observations, gets an ok/error as a response

```json
{
  "token": "d0d14d69-2f1f-42b3-ba11-36bfb22b323b",
  "req_token": "584c18df-2461-4121-95b0-3f0c7d1ae266",
  "msg_time": "2020-07-30T18:13:49.9532624Z",
  "action": "set_active_observers",
  "payload": {
    "state": ["agent_params"]
  }
}
```

## A state message

Provides the current state of the environment. This example has a variety of interactions defined

```json
{
  "token": "362d14c2-189a-4fd0-a4bf-b63796b89e63",
  "req_token": "00000000-0000-0000-0000-000000000000",
  "msg_time": "2020-10-27T01:13:58.2832191Z",
  "action": "state",
  "payload": {
    "game_mode": "learn",
    "environment_params": {
      "bounding_wall_color": [0.0, 0.5, 1.0],
      "light_intensity": 3.0,
      "predefined_map": 0,
      "map_size": [100, 100]
    },
    "agent_params": {
      "action_model": "BYVELOCITY",
      "agent_height": 0.999775767,
      "agent_width": 1.0,
      "max_linear_speed": 10.0,
      "max_angular_speed": 90.0,
      "observation_size": 84,
      "coordinates": [17.2518139, 27.50158],
      "heading": 210.596222
    },
    "image_params": {
      "zoom": 5.0,
      "yaw_subdivisions": 24,
      "vertical_subdivisions": 5
    },
    "objects": [
      {
        "model": "49",
        "class": "tree",
        "unique_name": "01d72db5-cb7e-4fe8-9393-518c2af9fda6",
        "coordinates": [34.4, 56.6],
        "color": [1.0, 1.0, 1.0],
        "motion_model": "stationary",
        "reward": 1.0,
        "range_stimulus_distance": 0.0
      },
      {
        "model": "4",
        "class": "Chair",
        "unique_name": "602eb0f5-1d0f-4e25-9221-979d2506e50f",
        "coordinates": [45.4, 54.5],
        "color": [0.1, 0.4, 1.0],
        "motion_model": "stationary",
        "reward": 150.0,
        "range_stimulus_distance": 0.0
      },
      {
        "model": "1",
        "class": "geometric",
        "unique_name": "302084fd-7bb6-4729-b6cd-96af2f776b74",
        "coordinates": [12.4, 4.5],
        "color": [1.0, 0.0, 0.0],
        "motion_model": "stationary",
        "reward": 0.25,
        "range_stimulus_distance": 2.0,
        "reward_once_stimulus": ["AgentInRange"],
        "destroy_stimulus": ["AgentCollide"]
      },
      {
        "model": "1",
        "class": "geometric",
        "unique_name": "680530b5-1a8f-415f-b1fc-23422a1311a9",
        "coordinates": [14.0, 8.0],
        "color": [1.0, 0.0, 0.0],
        "motion_model": "stationary",
        "reward": 0.0,
        "range_stimulus_distance": 0.0,
        "destroy_stimulus": ["AgentCollide"]
      },
      {
        "model": "1",
        "class": "geometric",
        "unique_name": "1f660bd0-b2cf-4acf-87c4-4b4e86477684",
        "coordinates": [14.0, 10.0],
        "color": [1.0, 1.0, 1.0],
        "motion_model": "stationary",
        "reward": 0.0,
        "range_stimulus_distance": 0.0,
        "destroy_stimulus": ["AgentInteract"]
      },
      {
        "model": "1",
        "class": "geometric",
        "unique_name": "f7f9e681-1624-4b82-85f0-a5134b178993",
        "coordinates": [14.0, 12.0],
        "color": [0.0, 0.0, 1.0],
        "motion_model": "stationary",
        "reward": 2.0,
        "range_stimulus_distance": 0.0,
        "reward_stimulus": ["AgentCollide"]
      },
      {
        "model": "1",
        "class": "geometric",
        "unique_name": "b0a00f13-8c6a-42bc-bfb8-da58b68986d6",
        "coordinates": [14.0, 14.0],
        "color": [0.0, 1.0, 1.0],
        "motion_model": "stationary",
        "reward": 3.0,
        "range_stimulus_distance": 0.0,
        "reward_once_stimulus": ["AgentInteract"]
      },
      {
        "model": "3",
        "class": "building",
        "unique_name": "e1be5a32-75aa-40e0-a307-e0b8ec9fc806",
        "coordinates": [12.4, 4.5],
        "color": [1.0, 1.0, 1.0],
        "motion_model": "stationary",
        "reward": 0.0,
        "range_stimulus_distance": 0.0
      },
      {
        "model": "49",
        "class": "tree",
        "coordinates": [33.4, 56.6],
        "color": [0.0, 0.0, 1, 0],
        "motion_model": "stationary",
        "reward": 0.0,
        "range_stimulus_distance": 0.0
      }
    ]
  }
}
```
