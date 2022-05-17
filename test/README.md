# Lifelong Learning Explorer (L2Explorer) Command-Line Interface

This directory contains a command-line interface for the L2Explorer environment. The CLI can be used to manually send messages on the side channels described in
[Channels.md](../docs/Channels.md) as well as perform agent actions within the environment described in the Action Space section [here](../README.md).

## Usage

The L2Explorer CLI is written in Python 3 and can be run from the command-line with the following arguments:

```
usage: l2explorer_cli.py [-h] [--debug] [--editor-mode]

optional arguments:
  -h, --help     show this help message and exit
  --debug        Enable debug mode for printing messages received on
                 L2Explorer channels
  --editor-mode  Connect to existing Unity editor
```

The `--debug` flag will enable all messages from the Unity environment to be printed to the console. This is disabled by default. The `--editor-mode` flag will prevent the L2ExplorerTask from creating a new instance of the L2Explorer environment, and will instead attempt to connect to an existing instance on the default editor port `5004`. In order for the editor mode to work properly, please ensure that the `L2EXPLORER_WORKER_ID` environment variable is set to `0`. Otherwise, `mlagents` will raise a `UnityEnvironmentException`. Editor mode is disabled by default and will try to create a new instance of the L2Explorer environment, so it necessary to have the `L2EXPLORER_APP` environment variable properly set to the full path of the downloaded unity executable.

### Commands

Once the CLI and L2Explorer environment have been initialized, you should see the L2Explorer prompt on the console:

```
l2explorer >
```

The following commands are available for execution and can be printed by entering `help` on the command-line:

```
Documented commands (type help <topic>):
========================================
action   channels  help   select_channel  step
channel  exit      reset  send_message
```

### Action

The `action` command takes two arguments: count and the actual action vector. The usage is shown below:

```
usage: action [-h] [-c COUNT] [-a ACTION [ACTION ...]]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        number of times to perform action
  -a ACTION [ACTION ...], --action ACTION [ACTION ...]
                        action tuple

Perform an action in the L2Explorer environment.
```

Example of performing 20 pickup steps with a linear velocity of 2 and an angular velocity of 0:

```
l2explorer > action -c 20 -a 2 0 1
```

### Channel

The `channel` command shows the currently selected channel for use when sending messages. If a channel has not yet been selected, the console will output a message stating so.

### Channels

The `channels` command lists the available channels for sending and receiving messages, also known as the side channels.

### Exit

The `exit` command exits the command-line application and gracefully closes the L2Explorer environment instance in the process. The following shorthand commands are also available from the command-line: `x`, `q`, and `Ctrl-C`.

### Reset

The `reset` command performs a reset in the L2Explorer environment. By default, this command will send the map defined in `default_map.json` unless a `reset_environment` action has been sent on the `Reset` side channel at any point. Once a successful `reset_environment` action has executed in a `send message` command, the L2Explorer CLI stores this map in a member variable and uses this map for resetting the L2Explorer environment.

### Select Channel

The `select channel` command allows the user to select a channel for sending messages. The selected channel is stored in a member variable and will be used as the default channel if one is not specified in the `send message` command. Note: whenever the `send message` command is executed, the channel used in the command will overwrite the channel member variable, which can be shown with `channel`.

### Send Message

The `send message` command has three potential arguments: file, channel, and message. The usage is shown below:

```
usage: send_message [-h] [-f FILE] [-c CHANNEL] [-m MESSAGE [MESSAGE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file containing messages for testing
  -c CHANNEL, --channel CHANNEL
                        channel to publish message on
  -m MESSAGE [MESSAGE ...], --message MESSAGE [MESSAGE ...]
                        message content
```

The `file` argument can be used to specify a JSON file containing a list of messages to send. An example JSON file with the proper format is provided in this directory (test_messages.json). Using the `file` argument will ignore the channel and message parameters.

For manually sending messages on the command-line, use the `channel` and `message` arguments to specify what to send on which side channel. If a channel has previously been selected using the `select channel` command, this argument is optional. If a `channel` is not provided and there hasn't been one set before, the application will prompt the user to select a channel to use. The `message` argument should be a compressed JSON with no newline characters. The specific contents of the message will vary depending on which channel has been selected. Please refer to the side channel documentation in docs/ for more details.

**Note**: The user may not be able to see responses from the Unity environment unless the `--debug` flag is set for the L2Explorer CLI.

#### Examples

Send a list of messages defined in a JSON file:

```
l2explorer > send_message -f test_messages.json
```

Send a reset environment message with one geometric object:

```
l2explorer > send_message -c Reset -m {"action":"reset_environment","payload":{"game_mode":"learn","max_steps":3000,"environment_params":{"bounding_wall_color":[0,100,255],"light_intensity":3.5,"predefined_map":"1","map_size":[100,100]},"agent_params":{"action_model":"byvelocity","agent_height":1.0,"agent_width":1.0,"max_linear_speed":15.0,"max_angular_speed":85.0,"observation_size":84,"coordinates":[10.0,10.0],"heading":0.0,"pickup_range":5.0},"image_params":{"zoom":5,"yaw_subdivisions":4,"vertical_subdivisions":22},"objects":[{"model":"1","class":"geometric","coordinates":[9.558255396623245,18.959918279645077],"color":[0.0,0.0,1.0],"motion_model":"stationary","reward_stimulus":["AgentInteract"],"destroy_stimulus":["AgentInteract"],"reward":100.0}]}}
```

Send an object create message with a tree (**Note**: the user may have to execute a manual `step` command in order to see changes occur):

```
l2explorer > send_message -c Reset -m {"action":"object_create","unique_name":"thing","payload":{"class":"tree","model":"49","coordinates":[33.4,56.6],"color":[0.0,0.0,1.0],"motion_model":"stationary"}}
```

Send a get debug categories command:

```
l2explorer > send_message -c Debug -m {"action":"get_debug_categories"}
```

Send a set debug categories command:

```
l2explorer > send_message -c Debug -m {"action":"set_debug_categories","payload":[{"category":"agent","active":true}]}
```

Send a get observers command:

```
l2explorer > send_message -c State -m {"action":"get_observers"}
```

Send a set observers command:

```
l2explorer > send_message -c State -m {"action":"set_active_observers","state":["agent_params"]}
```

### Step

The `step` command performs a step in the L2Explorer environment.
