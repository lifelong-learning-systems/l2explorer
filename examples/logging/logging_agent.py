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
import random
from collections import deque

import numpy as np
from l2explorer.l2explorer_env import L2ExplorerTask
from l2logger import l2logger

"""
Sample code illustrating how to start up and interact with 
an L2Explorer instance without using the learnkit (syllabus) 
interface.

This code integrates the l2logger library to directly produce logs for L2M
Run as:
python logging_agent.py -scenario test_scenario.json
"""


SCENARIO_DIR = 'test'
SCENARIO_INFO = {
    'author': 'JHU APL',
    'complexity': '1-low',
    'difficulty': '2-medium'
}
LOGGER_INFO = {
    'metrics_columns': ['reward']
}

def log_data(performance_logger, exp, results, status='complete'):
    seq = exp.sequence_nums
    worker = f'{os.path.basename(__file__)}_0'
    record = {
        'block_num': seq.block_num,
        'block_type': exp.block_type,
        'task_params': exp.params,
        'task_name': exp.task_name,
        'exp_num': seq.exp_num,
        'exp_status': status,
        'worker_id': worker
    }

    record.update(results)
    performance_logger.log_record(record)

class SequenceNums:
    def __init__(self, block, exp):
        self._block, self._exp = block, exp

    @property
    def block_num(self):
        return self._block

    @property
    def exp_num(self):
        return self._exp

class Experience:
    def __init__(self, agent, task_name, seq_nums: SequenceNums, params, block_type='train'):
        self._agent = agent
        self._task_name = task_name
        self._seq_nums = seq_nums
        self._block_type = block_type
        self._params = params
        self._update_model = (block_type == 'train')

    @property
    def task_name(self):
        return self._task_name

    @property
    def block_type(self):
        return self._block_type

    @property
    def sequence_nums(self):
        return self._seq_nums

    @property
    def param_string(self):
        return json.dumps(self._params)

    @property
    def params(self):
        return self._params

    def run(self, game):
        done = False
        num_steps = 0
        #load map from params
        with open(self._params["map"]) as fp:
            map = json.load(fp)
        state = game.reset(map)
        total_reward = 0
        while not done and num_steps < self._params["maxsteps"]:
            action = agent.process_step(state)
            state, reward, done, info = game.step(action)
            #If you are doing training, self._update_model==True
            if(self._update_model==True):
                pass #assemble necessary data for training
            # Each Visual observation is default size 84,84,3
            # There are three visual observations by default
            # 0: Depth Map
            # 1: RGB View
            # 2: Semantic Segmentation
            visual_obs = state["visual"]  # list of visual observation
            state_vector = state["state"]  # length 3 array with x,y,theta of agent in world frame
            total_reward = reward + total_reward
            num_steps += 1
        return {'reward': total_reward, 'debug_info': 'linearagent'}

class LinearAgent:
    def __init__(self, scenario):
        self._scenario = scenario
        self._init_queue()
        self._random = random.Random()

    def complete(self):
        return not len(self._exp_queue)

    def next_experience(self):
        assert (len(self._exp_queue))
        return self._exp_queue.popleft()

    # add all experiences to a deque for processing
    def _init_queue(self):
        self._exp_queue = deque()
        exp_num = -1
        for block_num, block in enumerate(self._scenario):
            block_type = block['type']
            for regime in block['regimes']:
                for _ in range(0, regime['count']):
                    exp_num += 1
                    task_name = regime['task']
                    seq = SequenceNums(block_num, exp_num)
                    exp = Experience(self, task_name, seq, regime['params'], block_type)
                    self._exp_queue.append(exp)

    def process_step(self, state):
        # action space: continuous values 
        # Linear movement: [-max_velocity,max_velocity]
        # Angular movement: [-max_angular_velocity,max_angular_velocity]
        # Pick up action: [-1,1] (if less than or equal to 0, no action is taken. 
        #    If greater than 0 the agent activates pick up action). Currently not used in examples given.

        #Default max values are linear speed 10, angular speed 90
        action = np.random.random_sample((3, 1))
        action[0] = 3.0
        action[1] = 0.0
        action[2] = 1.0
        return action

def run_scenario(agent, performance_logger):
    last_seq = SequenceNums(-1, -1)
    game = L2ExplorerTask()
    while not agent.complete():
        exp = agent.next_experience()
        cur_seq = exp.sequence_nums
        # check for new block
        if last_seq.block_num != cur_seq.block_num:
            print("new block:", cur_seq.block_num)
        results = exp.run(game)
        log_data(performance_logger, exp, results)

        last_seq = cur_seq
    game.close_env()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy agent for playing L2Explorer games with logging")
    parser.add_argument('-scenario', type=str, help="File with scenario JSON.")
    args = parser.parse_args()

    with open(args.scenario) as f:
        data = json.load(f)
    agent = LinearAgent(data['scenario'])
    SCENARIO_INFO['input_file'] = data
    performance_logger = l2logger.DataLogger(
        data['logging_base_dir'], SCENARIO_DIR, LOGGER_INFO, SCENARIO_INFO)
    run_scenario(agent, performance_logger)
