[Outline](Outline.md) -> [Channels](Channels.md) -> Debug Channel

# Debug Side Channels

This side channel provides the debug messages from the Unity app

# Debug Channel Messages

## Take Screenshot

Take a screenshot, save it to file.

```json
{
  "token": "05b78cc5-9ada-4993-9e66-b353ea131234", // Generate a new GUID for each message
  "msg_time": "2020-07-29T15:33:57.9251234Z", // Time message is sent
  "action": "save_screenshot", // Get the various categories
  "payload": {
    "filename": "blah.png", // PNG is the only encoding. If you use another extension, the content will still be PNG
    "upscale_factor": 1 // Integer values only, factor by which to increase resolution.
  }
}
```

## Get Categories

Request the debug categories that can be enabled or disabled, from Python to Unity

```json
{
  "token": "05b78cc5-9ada-4993-9e66-b353ea13c1c0", // Generate a new GUID for each message
  "msg_time": "2020-07-29T15:33:57.9256315Z", // Time message is sent
  "action": "get_debug_categories" // Get the various categories
}
```

## Category Listing

The debug categories available, returned by the Unity environment

```json
{
  "token": "b027045d-27bb-4e66-beb1-fe23a9e749e8",
  "req_token": "05b78cc5-9ada-4993-9e66-b353ea13c1c0",
  "msg_time": "2020-07-30T12:45:14.8099788Z",
  "action": "debug_categories",
  "payload": ["agent", "communications", "worldmaker", "academy"]
}
```

## Enable / Disable category messages

This message will enable or disable a category of debug information coming from the Unity application

```json
{
  "token": "05b78cc5-9ada-4993-9e66-b353ea13c1c0",
  "msg_time": "2020-07-29T15:33:57.9256315Z",
  "action": "set_debug_categories",
  "payload": [
    {
      "category": "agent", // Category
      "active": true // true | false
    }
  ]
}
```

## Debug Message

This message will be sent any time the Unity environment would have debugged a message to the console.

```json
{
  "token": "584c18df-2461-4121-95b0-3f0c7d1ae266", // generate new GUID for every message
  "msg_time": "2020-07-29T15:37:43.0908159Z", // Current time
  "action": "debug_message",
  "payload": {
    "category": "name", // Debug message category from debug category listing
    "level": "log|warning|error",
    "message": "Debug Message",
    "stack_trace": "The stack trace" // Stack traces get big, but can be handy
  }
}
```
