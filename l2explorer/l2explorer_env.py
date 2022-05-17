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
import sys
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import gym
import numpy as np
from gym import error, spaces
from mlagents_envs.base_env import DecisionSteps, TerminalSteps
from mlagents_envs.environment import UnityEnvironment

from l2explorer.l2explorer_channels import (DebugChannel, ResetChannel,
                                            StateChannel)

from .utils import get_l2explorer_app_location, get_l2explorer_worker_id

GymStepResult = Tuple[Dict, float, bool, Dict]

COMMUNICATION_TIMEOUT=10 #timeout in seconds


class UnityGymException(error.Error):
    """
    Any error related to the gym wrapper of ml-agents.
    """

    pass

class L2ExplorerTask(gym.Env):
    #Singleton Implementation of unity environment
    _env = None
    _reset_channel = None
    _debug_channel = None
    _state_channel = None
    _env_params = {}
    _MAX_INT = 2147483647  # Max int for Unity ML Seed

    @classmethod
    def close_env(cls):
        """Close the Unity environment and reset all environment variables"""
        if L2ExplorerTask._env:
            L2ExplorerTask._env.close()
        L2ExplorerTask._env = None
        L2ExplorerTask._env_params = {}


    #DO this in reset to allow seed to be set
    def __init__(self, debug=False, editor_mode=False, uint8_visual=False):
        # call reset() to begin playing
        self._workerid = get_l2explorer_worker_id()
        self.debug = debug
        if editor_mode:
            print('INFO: starting L2Explorer in editor mode')
            self._filename = None
        else:
            self._filename = get_l2explorer_app_location()
        self._observation_space = None
        self._action_space = None
        self._seed = None
        self._stepcount = 0
        self._maxsteps = 0
        self.use_visual = True  # L2 Explorer uses visual observations be default
        self._allow_multiple_visual_obs = True  # default to one obs for now
        self.uint8_visual = uint8_visual  # default to [0,255] uint8 valued pixels

    def seed(self, val):
        # integer seed required, convert
        self._seed = int(val) % L2ExplorerTask._MAX_INT

    def spawn_object(selfs, spawn_json, unique_name=None):
        # Spawn a new object with the "object_create" message
        # If unique_name is none, a random string name is generated
        # Otherwise, if unique_name is a string, it will be used
        # Before use, the environment must have been reset at least once to initialize L2explorerTask._env
        if L2ExplorerTask._env:
            # Send params, wait for params to be received
            L2ExplorerTask._reset_channel.send_json(
                {"action": "object_create", "payload": spawn_json, "unique_name": unique_name})
        else:
            print('WARNING: Cannot spawn objects until environment initialized')


    def reset(self, params):
        # Reset the environment
        #Params is a dict in the L2Explorer json format
        #create here so that we have the seed value set properly

        if not L2ExplorerTask._env:
            try:
                if not self._seed:
                    print('WARNING: seed not set, using default')
                    L2ExplorerTask._reset_channel = ResetChannel(self.debug)
                    L2ExplorerTask._debug_channel = DebugChannel(self.debug)
                    L2ExplorerTask._state_channel = StateChannel(self.debug)
                    L2ExplorerTask._env = UnityEnvironment(self._filename, self._workerid,
                                                           seed=1234, side_channels=[L2ExplorerTask._reset_channel, L2ExplorerTask._debug_channel, L2ExplorerTask._state_channel])
                    # set seed for procedural generation as well
                    np.random.seed(1234)
                else:
                    L2ExplorerTask._reset_channel = ResetChannel(self.debug)
                    L2ExplorerTask._debug_channel = DebugChannel(self.debug)
                    L2ExplorerTask._state_channel = StateChannel(self.debug)
                    L2ExplorerTask._env = UnityEnvironment(self._filename, self._workerid, seed=self._seed, side_channels=[
                                                           L2ExplorerTask._reset_channel, L2ExplorerTask._debug_channel, L2ExplorerTask._state_channel])
                    # set seed for procedural generation as well
                    np.random.seed(self._seed)
                L2ExplorerTask._env_params['filename'] = self._filename
                L2ExplorerTask._env_params['workerid'] = self._workerid

            except:
                print('ERROR: could not initialize unity environment, are filename correct and workerid not already in use by another unity instance?')
                raise
        elif L2ExplorerTask._env_params['filename'] != self._filename or L2ExplorerTask._env_params['workerid'] != self._workerid:
            #recreate environment
            L2ExplorerTask._env.close()
            try:
                if not self._seed:
                    L2ExplorerTask._reset_channel = ResetChannel(self.debug)
                    L2ExplorerTask._debug_channel = DebugChannel(self.debug)
                    L2ExplorerTask._state_channel = StateChannel(self.debug)
                    print('WARNING: seed not set, using default')
                    L2ExplorerTask._env = UnityEnvironment(self._filename, self._workerid,
                                                           seed=1234, side_channels=[L2ExplorerTask._reset_channel, L2ExplorerTask._debug_channel, L2ExplorerTask._state_channel])
                else:
                    L2ExplorerTask._reset_channel = ResetChannel(self.debug)
                    L2ExplorerTask._debug_channel = DebugChannel(self.debug)
                    L2ExplorerTask._state_channel = StateChannel(self.debug)
                    L2ExplorerTask._env = UnityEnvironment(self._filename, self._workerid, seed=self._seed, side_channels=[
                                                           L2ExplorerTask._reset_channel, L2ExplorerTask._debug_channel, L2ExplorerTask._state_channel])
                L2ExplorerTask._env_params['filename'] = self._filename
                L2ExplorerTask._env_params['workerid'] = self._workerid
            except:
                print('ERROR: could not initialize unity environment, are filename correct and workerid not already in use by another unity instance?')
                raise
       # Take a single step so that the brain information will be sent over
        if not L2ExplorerTask._env.get_behavior_names():
            self._env.step()

        self.visual_obs = None
        self._n_agents = 1 #L2explorer currently supports single agent

        # Check brain configuration
        if len(self._env.get_behavior_names()) != 1:
            raise UnityGymException(
                "There can only be one behavior in a UnityEnvironment "
                "if it is wrapped in a gym."
            )

        self.name = self._env.get_behavior_names()[0]
        self.group_spec = self._env.get_behavior_spec(self.name)

        #Send params, wait for params to be received
        L2ExplorerTask._reset_channel.send_json(
            {"action": "reset_environment", "payload": params})
        time.sleep(0.05)
        total_time = 0
        self._env.reset()  # reset, sleep, check for receipt of message
        time.sleep(0.05)

        while(not L2ExplorerTask._reset_channel.reset):
            time.sleep(0.001)
            total_time = total_time + 0.001
            if(total_time > COMMUNICATION_TIMEOUT):
                print('Timeout on Unity receipt of reset params')
                break
        # Reset message now received by Unity
        # Reset environment, get sizes of environment

        if self.group_spec.is_action_discrete():
            branches = self.group_spec.discrete_action_branches
            if self.group_spec.action_shape == 1:
                self._action_space = spaces.Discrete(branches[0])
            else:
                self._action_space = spaces.MultiDiscrete(branches)

        else:
            high = np.array([1] * self.group_spec.action_shape)
            self._action_space = spaces.Box(-high, high, dtype=np.float32)
        high = np.array([np.inf] * self._get_vec_obs_size())
        #Assume visual observations for now
        shape = self._get_vis_obs_shape()
        if self.uint8_visual:
            self._observation_space = spaces.Box(
                0, 255, dtype=np.uint8, shape=shape
            )
        else:
            self._observation_space = spaces.Box(
                0, 1.0, dtype=np.float32, shape=shape
            )

        # Select params for state query
        #If you submit an empty list, no state queries will be generated
        json_data = {}
        json_data["action"] = "set_active_observers"
        json_data["state"] = ["agent_params"]
        L2ExplorerTask._state_channel.request_keys(json_data)
        L2ExplorerTask._state_channel.state_dict = params

        """Resets the state of the environment and returns an initial observation.
        Returns: observation (object): the initial observation of the
        space.
        """

        # reset step count
        self.game_over = False
        self._stepcount = 0
        self._maxsteps = params['max_steps']

        decision_step, _ = self._env.get_steps(self.name)
        # First frame is badly initialized and tilted.
        # Step once to discard  bad observation
        res: GymStepResult = self._single_step(decision_step)

        # Now step for first observation of properly initialized enivronment
        res: GymStepResult = self._single_step(decision_step)
        self._env_info = res
        return res[0]

    def render(self):
        '''Render by returning visual observation 1 for display'''
        return self._env_info.visual_observations[0]

    def step(self, action: List[Any]) -> GymStepResult:
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        In the case of multi-agent environments, these are lists.
        Args:
            action (object/list): an action provided by the environment
        Returns:
            observation (object/list): agent's observation of the current environment
            reward (float/list) : amount of reward returned after previous action
            done (boolean/list): whether the episode has ended.
            info (dict): contains auxiliary diagnostic information, including BatchedStepResult.
        """
        if not self.game_over:
            spec = self.group_spec
            action = np.array(action).reshape((self._n_agents, spec.action_size))
            self._env.set_actions(self.name, action)

            step_result = self._env.step()

            #n_agents = step_result.n_agents()
            #self._check_agents(n_agents)
            decision_step, terminal_step = self._env.get_steps(self.name)
            if len(terminal_step) != 0:
                single_res = self._single_step(terminal_step)
                # The agent is done
                self.game_over = True
                self._stepcount = self._stepcount + 1
                return single_res
            else:
                single_res = self._single_step(decision_step)
                if self._stepcount > self._maxsteps:
                    self.game_over = True
                    single_res = (single_res[0], single_res[1], True, single_res[3])
                else:
                    self.game_over = single_res[2]
                self._stepcount = self._stepcount + 1
                return single_res
        else:
            print('INFO: step called after max_steps reached is true, reset env')
            return {}, 0, True, {}

    def _single_step(self, info: Union[DecisionSteps, TerminalSteps]) -> GymStepResult:
        if self.use_visual:
            visual_obs = self._get_vis_obs_list(info)
            if len(visual_obs) > 0:
                if self._allow_multiple_visual_obs:
                    visual_obs_list = []
                    for obs in visual_obs:
                        visual_obs_list.append(self._preprocess_single(obs[0]))
                    self.visual_obs = visual_obs_list
                else:
                    self.visual_obs = self._preprocess_single(visual_obs[0][0])
            else:
                # default black background
                self.visual_obs = np.zeros(self._get_vis_obs_shape())
                print('INFO: generating default black background')

            default_observation = self.visual_obs
        elif self._get_vec_obs_size() > 0:
            default_observation = self._get_vector_obs(info)[0, :]
        else:
            raise UnityGymException(
                "The Agent does not have vector observations and the environment was not setup "
                + "to use visual observations."
            )
        done = isinstance(info, TerminalSteps)
        observation = {}
        observation["visual"] = default_observation
        observation["state"] = self._get_vector_obs(info)[0, 1:40]
        return (observation, info.reward[0], done, {"step": info})

    def _preprocess_single(self, single_visual_obs: np.ndarray) -> np.ndarray:
        if self.uint8_visual:
            return (255.0 * single_visual_obs).astype(np.uint8)
        else:
            return single_visual_obs

    def _get_n_vis_obs(self) -> int:
        result = 0
        for shape in self.group_spec.observation_shapes:
            if len(shape) == 3:
                result += 1
        return result

    def _get_vis_obs_shape(self) -> Optional[Tuple]:
        for shape in self.group_spec.observation_shapes:
            if len(shape) == 3:
                return shape
        return None

    def _get_vis_obs_list(
        self, step_result: Union[DecisionSteps, TerminalSteps]
    ) -> List[np.ndarray]:
        result: List[np.ndarray] = []
        for obs in step_result.obs:
            if len(obs.shape) == 4:
                result.append(obs)
        return result

    def _get_vector_obs(
        self, step_result: Union[DecisionSteps, TerminalSteps]
    ) -> np.ndarray:
        result: List[np.ndarray] = []
        for obs in step_result.obs:
            if len(obs.shape) == 2:
                result.append(obs)
        return np.concatenate(result, axis=1)

    def _get_vec_obs_size(self) -> int:
        result = 0
        for shape in self.group_spec.observation_shapes:
            if len(shape) == 1:
                result += shape[0]
        return result

    def _check_agents(self, n_agents: int) -> None:
        if self._n_agents > 1:
            raise UnityGymException(
                "There can only be one Agent in the environment but {n_agents} were detected."
            )
