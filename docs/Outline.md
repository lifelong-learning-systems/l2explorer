# Overview of Unity environment

The L2Explorer environment is hosted in a Unity application and controlled externally by the learnkit python code.
This document describes how environment specifications from the learnkit, called a 'reset message' in Unity ML Agents, are handled in the compiled application.
Also included is an overview of the agent's inputs and observations/outputs.

There is a [Changelog](Changelog.md) available as the environment develops

In this document:

<!-- TOC -->

- [1. Communication between Unity and Python](#Communication-between-Unity-and-Python)
- [2. Description of fields](#Description-of-fields)
- [3. Agent-Object interactions](#Agent-Object-interactions)
- [4. Available models](#Available-models)
- [5. Optional starter maps](#Optional-starter-maps)
- [6. Agent movement](#Agent-movement)
- [7. Visual observations](#Visual-observations)
- [8. Custom observation](#Custom-observation)
- [9. Vector observation](#Vector-observation)
<!-- /TOC -->

## Communication between Unity and Python

L2M uses the "Side Channels" feature of ML-Agents to communicate between the Unity executable and the python code.

[L2M Channels and Messages](Channels.md)

## Agent-Object interactions

As of 0.42, the Agent-Object interactions have been significantly reworked.

There a currently three actions that an object can take:

- Reward: The object can provide a reward to the agent
- Reward Once: The object can provide a reward to the agent, and then set its reward value to zero
- Destroy: The object destroys itself

For any of these actions, there needs to be one or more stimuli to trigger the action. As of 0.42 there are two stimuli

- Collision: When the agent intersects with the object, the agent
- Interact: When the object is within a 1m cube to the front of the agent, and the agent issues the interact action

## Model Assets Library

As of 0.47, the models available for an environment have been separated from the main executable. This allows organizations to add/refine/remove available content as needed. The application selects an asset file based on the current operating system, model class, and model ID.

On startup, the L2 Explorer application will look a file named `l2explorer-config.json` in the same directory as the executable. If L2 Explorer cannot find a config file, it will create an empty one.

Example `l2explorer-config.json`

```json
{ "libraryPath": "C:\\l2mAssets" }
```

If the library path value is null or the directory does not exist, it is a critical failure, and a large error message will be displayed to the user.

If the directory does exist, the application will attempt to load requested models from the available assets. The OS will be detected by the application, and will either be `Windows` or `Linux`. It reads assets using the following naming convention:

```
{libraryPath}\{platform}\{class}{id}
```

If a requested asset does not exist, the application will fail gracefully and continue to execute.

## Agent movement

The agent mover will always take in 3 floats as as continuous action vector `<a, b, c>`. The "action_model" field determines how these inputs are used.

### ByVelocity

**a** defines the meters per second that the agent will move this frame. Positive moves it forward, negative moves it backwards.

**b** defines the degrees per second the agent will rotate this frame. Positive values indicate a right-turn, negative values are a left-turn

**c** activates a pick-up action if the value is above 0.5. Below 0.5 is a no-op.

### ByWaypoint

**a** defines the x-value of the coordinate that the agent body will navigate towards

**b** defines the y-value of the coordinate.

**c** defined degrees per second that the camera turns; positive is a right-turn, negative is a left-turn.

### OnRails

Agent inputs have no effect. The mover will automatically start touring all objects with a positive reward, navigating to them and picking up if possible.

### None

Inputs have no effect. This mode is used for image-collection mode and isn't suitable for RL.

## Visual observations

### Segmented observation

In this view, objects are recolored according to their layer, which defines reward category (such as hazard or target). The following defines what colors match what layer.

Note that decimal RGB values are truncated.

object layer	| color name 	| 0-1 RGB 			| 0-255 RGB			| description
----------------|---------------|-------------------|-------------------|---------------------------------------------------------------------------------------------------------------------
skybox 			| black 		| `[0, 0, 0]`		| `[0, 0, 0]` 		| The empty sky above the arena
default			| white 		| `[1, 1, 1]`		| `[255, 255, 255]`	| Any object not accounted for by spawning mechanism - this can include objects that are part of a loaded map.
building		| pale green	| `[0.69, 1, 0.69]`	| `[178, 255, 178]` | Any object spawned in the 'building' class
target 			| teal blue		| `[0, 1, 1]`		| `[0, 255, 255]` 	| Any object with a positive reward
neutral			| soft pink		| `[1, 0.69, 0.69]`	| `[255, 178, 178]` | Any object with a reward of zero
hazard 			| magenta		| `[1, 0, 1]`		| `[255, 0, 255]` 	| Any object with a negative reward.

#### FPV

This is the normal first-person view of the agent. It is in RGB color. The resolution is defined by the `observation_size` field in the reset message. The FPV is always square.

#### Depth Observation

This view uses color data to show the distance of objects in the scene from the agent's camera. The image is RGB encoded, but always is in greyscale colors.

As a given pixel represents an object closer to the agent, the depth view will draw that pixel darker, approaching RGB value of `[0,0,0]`. As the object grows farther from the agent, its color approaches white, RGB `[1, 1, 1]`

The cutoff distance, after which all objects will appear white, is 100 meters away from the agent.

## Vector observation

The vector observation is sent every frame. It has a length of 1. The value is the object ID of any item collected in the relevant frame. This information is made redundant by the recent addition of a Custom observation, described below.

## Custom observation

We utilize a Google Protobuf message to send a custom structured observation every frame. The message contains the agent's position, heading, and the object ID of any object collected in the relevant frame.

````protobuf
syntax = "proto3";

option csharp_namespace = "MLAgents.CommunicatorObjects";
package communicator_objects;

message CustomObservation {
    float agent_x = 1;
    float agent_y = 2;
    float agent_heading = 3;
    int32 interaction_object_id = 4;
}
````
