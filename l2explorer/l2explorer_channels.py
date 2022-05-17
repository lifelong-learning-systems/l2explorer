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

import json
import time
import uuid
from datetime import datetime

from mlagents_envs.side_channel.side_channel import (IncomingMessage,
                                                     OutgoingMessage,
                                                     SideChannel)


# Create the StringLogChannel class
class ResetChannel(SideChannel):
    # Sends json string with reset parameters
    def __init__(self, debug=False) -> None:
        super().__init__(uuid.UUID("621f0a70-4f87-11ea-a6bf-784f4387d1f7"))
        self.debug = debug
        self.reset = False

    def on_message_received(self, msg: IncomingMessage) -> None:
        """
        Note: We must implement this method of the SideChannel interface to
        receive messages from Unity
        Should receive and print "Reset Configured" if reset params received
        """
        # We simply read a string from the message and print it.
        self.reset = True

        if self.debug:
            print(msg.read_string())

    def send_json(self, data: dict) -> None:
        # Add the string to an OutgoingMessage
        if data.keys() >= {"action", "payload"}:
            json_data = {}
            json_data["token"] = str(uuid.uuid1())
            json_data["action"] = data["action"]
            json_data["msg_time"] = datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%dT%H:%M:%S')
            json_data["payload"] = data["payload"]

            #set unique name for spawning objects
            if json_data["action"] == "object_create":
                if "unique_name" in data:
                    json_data["unique_name"] = data["unique_name"]
                else:
                    json_data["unique_name"] = str(uuid.uuid1())

            msg = OutgoingMessage()
            msg.write_string(json.dumps(json_data))

            # We call this method to queue the data we want to send
            self.reset = False
            super().queue_message_to_send(msg)
        else:
            print(f"Error in creating reset message: action or payload missing")

class DebugChannel(SideChannel):
    # Builds on ml-agents example side channel
    # Can write messages, which will be recorded in the Unity logs with the From python: prefix
    # Receives error messages from unity, prints with From Unity: prefix
    def __init__(self, debug=False) -> None:
        super().__init__(uuid.UUID("c5fba0b5-6392-4433-a95f-cdec6b0061e1"))
        self.debug = debug

    def on_message_received(self, msg: IncomingMessage) -> None:
        """
        Note: We must implement this method of the SideChannel interface to
        receive messages from Unity
        """
        # We simply read a string from the message and print it.
        data = json.loads(msg.read_string())

        if self.debug:
            print(data)

    def send_string(self, data: dict) -> None:
        # Add the string to an OutgoingMessage
        if "action" in data:
            json_data = {}
            json_data["token"] = str(uuid.uuid1())
            json_data["action"] = data["action"]
            json_data["msg_time"] = datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%dT%H:%M:%S')
            if json_data["action"] in ["save_screenshot", "set_debug_categories"]:
                try:
                    json_data["payload"] = data["payload"]
                except Exception as e:
                    print("Error in creating debug message: ", e)
                    return

            msg = OutgoingMessage()
            msg.write_string(json.dumps(json_data))
            # We call this method to queue the data we want to send
            super().queue_message_to_send(msg)
        else:
            print(f"Error in creating debug message: action missing")


class StateChannel(SideChannel):
    # Allows us to query specific values that were specified in the reset json, and get a response
    # Specified keys must be valid keys in the reset json
    # Defaults to returning all values
    def __init__(self, debug=False) -> None:
        super().__init__(uuid.UUID("37715121-3bce-45ff-966d-680586560a5d"))
        self.debug = debug
        self.state_dict = {}  # empty dictionary of states

    def on_message_received(self, msg: IncomingMessage) -> None:
        """
        Note: We must implement this method of the SideChannel interface to
        receive messages from Unity

        """
        # Fill dictionary with json
        data_dict = json.loads(msg.read_string())
        self.state_dict = data_dict["payload"]

        if self.debug:
            print(data_dict)

    def request_keys(self, data: dict) -> None:
        # Add the string to an OutgoingMessage
        if "action" in data:
            json_data = {}
            json_data["token"] = str(uuid.uuid1())
            json_data["action"] = data["action"]  # set_active_observers
            json_data["msg_time"] = datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%dT%H:%M:%S')
            if json_data["action"] == "set_active_observers":
                try:
                    json_data["payload"] = {}
                    json_data["payload"]["state"] = data["state"]
                except Exception as e:
                    print("Error in creating state message: ", e)
                    return

            # print(json.dumps(json_data))
            msg = OutgoingMessage()
            msg.write_string(json.dumps(json_data))
            # We call this method to queue the data we want to send
            super().queue_message_to_send(msg)
        else:
            print(f"Error in creating state message: action missing")        
