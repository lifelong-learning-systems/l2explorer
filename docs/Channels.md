[Outline](Outline.md) -> Channels

# Side Channels and messages

Within L2M, there are a number of side channels designed to provide different kinds of messages between the L2M Explorer and the ML tools that use it.

All messages should have a token GUID, an action, a timestamp, and in almost all cases, a payload.

---

## An acknowledgement Message

```json
{
  "token": "a62cdbe8-9e96-4761-85a4-e3c2f1f1e892", // a new message guid
  "req_token": "00000000-0000-0000-0000-000000000000", // The token the system is responding to, or 0s if no token found
  "msg_time": "2020-07-29T15:41:39.8418368Z", // Time of response
  "action": "ok" // Everything's ok
}
```

## An Error Message

In the event that a channel gets an action it doesn't understand, it will generate an error message.

```json
    {
        "token":"a62cdbe8-9e96-4761-85a4-e3c2f1f1e892", // a new message guid
        "req_token":"00000000-0000-0000-0000-000000000000", // The token the system is responding to, or 0s if no token found
        "msg_time":"2020-07-29T15:41:39.8418368Z", // Time of response
        "action":"error", // It's an error message
        "payload":["Action not understood"]} // a list of error messages
    }
```

---

## Debug Channel

This channel provides debug information that the L2M Explorer application provides.

[Debug Channel Details](DebugChannel.md)

Channel GUID: c5fba0b5-6392-4433-a95f-cdec6b0061e1

---

## Reset Channel

The reset channel will reset the environment to a new configuration. This channel can also be used to dynamically spawn new objects during a game.

[Reset Channel Details](ResetChannel.md)

Channel GUID: 621f0a70-4f87-11ea-a6bf-784f4387d1f7

---

## State Channel

The state channel is for configuring and passing game state information

[State Channel Details](StateChannel.md)

Channel GUID: 37715121-3bce-45ff-966d-680586560a5d

## Interaction models 

Several options area available in the reset json to define object interactions. Examples are given in 

[Interaction Details](Interactions.md)

