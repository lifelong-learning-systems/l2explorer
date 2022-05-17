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

import argparse
import json
import os
import traceback
from cmd import Cmd
from typing import Any, List

import inquirer
import numpy as np
from l2explorer.l2explorer_env import L2ExplorerTask

channels = ['Reset', 'Debug', 'State']


class L2ExplorerPrompt(Cmd):
    prompt = "l2explorer > "
    intro = "Welcome to the L2Explorer command line tool! Type ? to list commands"

    def __init__(self, debug=False, editor_mode=False):
        """L2ExplorerPrompt initializing function."""
        super().__init__()

        # Initialize variables
        self.channel = ''
        self.map = None

        # Initialize L2Explorer environment
        self._env = L2ExplorerTask(debug, editor_mode)
        self.init_env()

        # Initialize the argument parser for sending messages
        self.message_parser = argparse.ArgumentParser(prog="send_message")
        self.action_parser = argparse.ArgumentParser(prog="action")
        self.init_parsers()

    def init_env(self, map=None):
        # Load default map
        if map is None:
            mapname = 'default_map.json'
            with open(mapname) as f:
                map = json.load(f)

        self._env.reset(map)
        self.name = self._env._env.get_behavior_names()[0]
        self.group_spec = self._env._env.get_behavior_spec(self.name)
        self._n_agents = 1

        # Step multiple times to update environment
        for i in range(4):
            self.do_step()

    def init_parsers(self):
        """Initialize argument parsers for L2Explorer channel tester.

        :return: Status.
        """
        # Initialize message parser
        self.message_parser.add_argument('-f', '--file',
                                         help='file containing messages for testing')
        self.message_parser.add_argument('-c', '--channel',
                                         help='channel to publish message on')
        self.message_parser.add_argument('-m', '--message', nargs='+',
                                         help='message content')

        # Initialize action parser
        self.action_parser.add_argument('-c', '--count', type=int, default=1,
                                        help='number of times to perform action')
        self.action_parser.add_argument('-a', '--action', nargs='+', type=int,
                                        help='action tuple')

        return True

    def do_exit(self, argv=None):
        """Exits L2ExplorerPrompt after cleanup.

        :param argv: Ignored.
        :return: Exit status.
        """
        print("\nExiting L2Explorer CLI...\n")

        return True

    def help_exit(self):
        """Helper function for exit.

        :return: None.
        """
        print("\nExit the application. Shorthand: x, q, Ctrl-C.\n")

    def do_channels(self, argv=None):
        """List the available channels for sending and receiving messages.

        :param argv: Ignored.
        :return: None.
        """
        print("")
        for channel in channels:
            print(f"   {channel}")
        print("")

    def help_channels(self):
        """Helper function for channels.

        :return: None.
        """
        print("\nList the available channels for sending and receiving messages.\n")

    def do_select_channel(self, argv=None):
        """Display an interactive list for selecting a channel for sending and receiving messages.

        :param argv: Ignored.
        :return: None.
        """
        question = [
            inquirer.List('channel',
                          message="What channel would you like to communicate on?",
                          choices=channels,
                          carousel=True
                          ),
        ]
        print("")
        self.channel = inquirer.prompt(question)["channel"]

    def help_select_channel(self):
        """Helper function for select channel.

        :return: None.
        """
        print("\nSelect a channel for sending messages.\n")

    def do_channel(self, argv=None):
        """Display the currently selected channel.

        :param argv: Ignored.
        :return: None.
        """
        if self.channel:
            print(f"\n  Channel: {self.channel}\n")
        else:
            print("\nA channel has not been selected yet.\n")

    def help_channel(self):
        """Helper function for channel.

        :return: None.
        """
        print("\nShow the currently selected channel.\n")

    def do_reset(self, argv=None):
        """Perform a reset in the L2Explorer environment.

        :param argv: Ignored.
        :return: None.
        """
        self.init_env(self.map)

    def help_reset(self):
        """Helper function for reset.

        :return: None.
        """
        print("\nPerform a reset in the L2Explorer environment.\n")

    def do_step(self, argv=None):
        """Perform a step in the L2Explorer environment.

        :param argv: Ignored.
        :return: None.
        """
        self._env._env.step()

    def help_step(self):
        """Helper function for step.

        :return: None.
        """
        print("\nPerform a step in the L2Explorer environment.\n")

    def do_action(self, argv=None):
        """Perform an action in the L2Explorer environment.

        :param argv: The action parameters.
        :return: None.
        """
        try:
            # Parse the argument vector
            args = self.action_parser.parse_args(argv.split())

            if args.action:
                for _ in range(0, args.count):
                    _, reward, _, _ = self._env.step(args.action)
                    print(f'Reward: {reward}')
        except Exception as e:
            print(e)
            traceback.print_exc()
            pass
        except SystemExit:
            pass

    def help_action(self):
        """Helper function for action.

        :return: None.
        """
        self.action_parser.print_help()
        print("\nPerform an action in the L2Explorer environment.\n")

    def send_message(self, channel: str, message: dict):
        if channel == 'Reset':
            action = message.get('action', '')

            if action == 'reset_environment':
                self.map = message.get('payload', None)
                self.do_reset()
            elif action == 'object_create':
                self._env._reset_channel.send_json(message)
                self.do_step()
            else:
                print(f"Invalid reset action: {action}")
        elif channel == 'Debug':
            self._env._debug_channel.send_string(message)
            self.do_step()
        elif channel == 'State':
            self._env._state_channel.request_keys(message)
            self.do_step()
        else:
            print(f"Unimplemented channel: {channel}")

    def do_send_message(self, argv=None):
        """Send/receive a message on the selected channel.

        :param argv: The message parameters.
        :return: None.
        """
        try:
            # Parse the argument vector
            args = self.message_parser.parse_args(argv.split())

            # Check if test file is specified
            if args.file:
                # Parse file
                with open(args.file) as f:
                    data = json.load(f)

                    # Iterate over test messages and send over side-channel
                    for test in data["tests"]:
                        self.send_message(test["channel"], test["message"])
            else:
                # Get channel
                self.get_channel(args.channel)

                # Send message on proper channel
                if args.message:
                    self.send_message(self.channel, json.loads(''.join(args.message)))
                else:
                    print("Missing argument: -m --message")

        except Exception as e:
            print(e)
            traceback.print_exc()
            pass
        except SystemExit:
            pass

    def help_send_message(self):
        """Helper function for send message.

        :return: None.
        """
        self.message_parser.print_help()

    def get_channel(self, channel_arg):
        """Check if channel has been selected or prompt user to select one.

        :param channel_arg: The channel argument given on the command line.
        :return: Channel
        """
        try:
            if channel_arg in channels:
                self.channel = channel_arg
            elif not self.channel:
                self.do_select_channel()
        except:
            pass

        return self.channel

    def default(self, argv):
        """Default handler if unknown command is entered on the command line.

        :param argv: The line entered on the command line.
        :return: Status.
        """
        if argv == 'x' or argv == 'q':
            # Check for shorthand exit commands
            return self.do_exit(argv)
        else:
            print("Unknown command: {}".format(argv))


if __name__ == "__main__":
    try:
        # Initialize argument parser
        parser = argparse.ArgumentParser()
        parser.add_argument('--debug', action='store_true',
                            help='Enable debug mode for printing messages received on L2Explorer channels')
        parser.add_argument('--editor-mode', action='store_true',
                            help='Connect to existing Unity editor')

        # Parse arguments
        args = parser.parse_args()

        # Change directory to directory of current file
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Start L2Explorer Prompt
        L2ExplorerPrompt(args.debug, args.editor_mode).cmdloop()
    except KeyboardInterrupt:
        print("\nExiting L2Explorer CLI...")
        # Close L2Explorer environment gracefully
        L2ExplorerTask.close_env()
