[Outline](Outline.md) -> Interactions

As of 0.42, the Agent-Object interactions have been significantly reworked.

There a currently three actions that an object can take:

- Reward: The object can provide a reward to the agent
- Reward Once: The object can provide a reward to the agent, and then set its reward value to zero
- Destroy: The object destroys itself

For any of these actions, there needs to be one or more stimuli to trigger the action. As of 0.42 there are two stimuli

- Collision: When the agent intersects with the object, the agent
- Interact: When the object is within a 1m cube to the front of the agent, and the agent issues the interact action

In the `objects` fields, this is specified by
  - `reward` : float `(-inf, inf)` : How much reward to give the agent for interacting with this object. Rewards can be repeated under certain circumstances - see 'Object interactions' for more information.
  - `range_stimulus_distance` : float `(0, inf)` : At what distance is `AgentInRange` triggered
  - `reward_stimulus`: string[] : What stimuli will cause this object to provide its reward to the agent? This is for recurring rewards / penalties
  - `reward_once_stimulus`: string[] : What stimuli will cause this object to provide its reward to the agent? This is for one-shot rewards / penalties (the reward will be set to zero after the first time it is provided to the agent)
  - `destroy_stimulus`: string[] : What stimuli will cause this object to be destroyed?

## Object Interaction Options, used for Reward Stimulus 

- AgentCollide : Triggers when the agent collides with the object
- AgentInteract : Triggers when the agent explicitly attempts to interact with the object while it is in the agent's interaction volume
- AgentInRange : Triggers when the agent is within this range (centroid to centroid in 3D space, so the value should be larger than the radius of the object + the radius of the agent)

## Examples

{"model": "1", "class": "geometric", "coordinates": [
                10.406359009231341,
                30.715634786321754
            ], "color": [
                0.0,
                0.0,
                1.0
            ], "motion_model": "stationary", "reward_stimulus": ["AgentCollide","AgentInteract"
            ],"destroy_stimulus": ["AgentInteract"
            ], "reward": 100.0
        }
        
{"model": "1", "class": "geometric", "coordinates": [
                10.406359009231341,
                30.715634786321754
            ], "color": [
                0.0,
                0.0,
                1.0
            ], "motion_model": "stationary", "reward_stimulus": ["AgentCollide"
            ],"destroy_stimulus": [], "reward": 100.0
        }
        
{"model": "1", "class": "geometric", "coordinates": [
                10.406359009231341,
                30.715634786321754
            ], "color": [
                0.0,
                0.0,
                1.0
            ], "motion_model": "stationary",
            "destroy_stimulus": [
                "AgentInRange"
            ],
            "reward_once_stimulus": [
                "AgentInRange"
            ],
            "range_stimulus_distance": 4,
            "reward": 100.00
        }