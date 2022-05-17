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
import random
import sys

import l2explorer
import numpy as np
from l2explorer.l2explorer_env import L2ExplorerTask

"""
Sample code illustrating how to start up and interact with 
an L2Explorer instance without using the learnkit (syllabus) 
interface.
Example usage: 
python linear_agent.py -reps 3 -maxsteps 200 -jsonfile map_findobjects_0.json
"""


class LinearAgent():
    def __init__(self):
        self._random = random.Random()

    def process_step(self, state):
        # action space: continuous values
        # Linear movement: [-max_velocity,max_velocity]
        # Angular movement: [-max_angular_velocity,max_angular_velocity]
        # Pick up action: [-1,1] (if less than or equal to 0, no action is taken.
        #    If greater than 0 the agent activates pick up action). Currently not used in examples given.

        # Default max values are linear speed 10, angular speed 90
        action = np.random.random_sample((3, 1))
        action[0] = 3.5
        action[1] = 0.0
        action[2] = 1.0
        return action


def play_linear_agent(game, params, max_steps=500):
    """ Play a game until completion with random agent"""
    agent = LinearAgent()
    done = False
    num_steps = 0
    state = game.reset(params)
    while not done and num_steps < max_steps:
        action = agent.process_step(state)
        state, reward, done, info = game.step(action)
        # Each Visual observation is default size 84,84,3
        # There are three visual observations by default
        # 0: Depth Map
        # 1: RGB View
        # 2: Semantic Segmentation
        visual_obs = state["visual"]  # list of visual observation
        state_vector = state["state"]  # length 3 array with x,y,theta of agent in world frame
        if reward > 0:
            print(f'Reward is {reward}')
        num_steps += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy agent for playing L2Explorer games")
    parser.add_argument('-reps', type=int, default=3, help="Number of times to play the game (def=3)")
    parser.add_argument('-maxsteps', type=int, default=200,
                        help="Max number of time steps (def=200). Set to 0 to disable.")
    parser.add_argument('-jsonfile', type=str, help="File to environment JSON.")
    parser.add_argument('-uint8', type=bool, default=False,
                        help="True to use uint8 observations, false to use float observations.")
    args = parser.parse_args()

    # load param
    with open(args.jsonfile) as json_file:
        parsed_json = json.load(json_file)

    max_steps = sys.maxsize if args.maxsteps == 0 else args.maxsteps

    game = L2ExplorerTask(uint8_visual=args.uint8)
    try:
        for _ in range(args.reps):
            play_linear_agent(game, params=parsed_json, max_steps=max_steps)
    finally:
        game.close_env()