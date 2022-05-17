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

"""
GUI to allow a person to as the machine learning agent (see observations, respond with actions).
"""
import sys
import argparse
import numpy as np
import cv2
import tkinter as tk
import json

import l2explorer
from l2explorer.l2explorer_env import L2ExplorerTask



class ParameterGui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._params = {}
        self._agent = None
        self._master = master
        self.create_widgets()
        self.pack()

    def set_agent(self, runner):
        self._agent = runner

    def create_widgets(self):
        self._window = tk.PanedWindow(self, orient=tk.VERTICAL)
        #
        self._info_pane = tk.LabelFrame(self._window, text="Current Status")
        tk.Label(self._info_pane, text="Action [linear, angular, pickup]").pack(side="left")
        self._action_var = tk.StringVar(self._info_pane)
        self._action_var.set("0 0 0")
        tk.Label(self._info_pane, textvariable=self._action_var).pack(side="right")
        self._info_pane.pack(fill=tk.X)
        #
        self._env_pane = tk.LabelFrame(self._window, text="Environment")
        tk.Label(self._env_pane, text="Light Intensity:").pack(side="left")
        tk.Scale(self._env_pane, from_=0.1, to=5.0, orient=tk.HORIZONTAL, resolution=0.2,
                command = lambda val: self._set_param_value("light_intensity", float(val))).pack(side="right")
        self._env_pane.pack(fill=tk.X)
        #
        self._agent_pane = tk.LabelFrame(self._window, text="Agent")
        self._obstype_var = tk.StringVar(self._agent_pane)
        self._obstype_var.set("RGB")
        self._obstype_var.trace(mode="w", callback=self._change_observation_type)
        tk.Label(self._agent_pane, text="Observation Type").pack(side="left")
        tk.OptionMenu(self._agent_pane, self._obstype_var, "RGB", "Depth", "Semantic").pack(side="right")
        self._agent_pane.pack(fill=tk.X)
        #
        self._misc_pane = tk.LabelFrame(self._window, text="")
        self.reset = tk.Button(self._misc_pane, text="Reset Environment", command = self._do_reset)
        self.reset.pack(side="left")
        self.quit = tk.Button(self._misc_pane, text="Quit", command = self._do_quit)
        self.quit.pack(side="right")
        self._misc_pane.pack(fill=tk.X)
        #
        self._window.pack()


    def update_action_value(self, action):
        action_str = "{0:.2f} {1:.2f} {2}".format(*action)
        self._action_var.set(action_str)

    def _set_param_value(self, key, value):
        self._params[key] = value

    def _change_observation_type(self, *args):
        val = self._obstype_var.get()
        mapping = {"RGB": ImageType.RGB_IMAGE, "Depth": ImageType.DEPTH_IMAGE, "Semantic": ImageType.SEMANTIC_IMAGE}
        if self._agent:
            self._agent.set_image_type(mapping[val])

    def _do_reset(self):
        if self._agent:
            self._agent.reset_env(self._params)

    def _do_quit(self):
        if self._agent:
            self._agent.quit_env()
        else:
            self.close()

    def close(self):
        self._master.destroy()

    def process_events(self):
        self.update_idletasks()
        self.update()

    @staticmethod
    def make_gui():
        """
        Sample usage:
            gui = ParameterGui.make_gui()
            while True:
                gui.process_events()
        This will also work
            gui = ParameterGui.make_gui()
            gui.mainloop()
        """
        root = tk.Tk()
        gui = ParameterGui(master=root)
        return gui


#-------------------------------------------------------

import enum
class UserInput(enum.IntEnum):
    LEFT = 1
    RIGHT = 2
    FORWARD = 3
    BACK = 4
    PICKUP = 5
    QUIT = 20
    def __int__(self):
        return self.value

class ImageType(enum.Enum):
    # the values of the enum correspond to order of the images
    # in the observation returned from L2Explorer
    RGB_IMAGE = 0
    DEPTH_IMAGE = 1
    SEMANTIC_IMAGE = 2


class CV2ImageDisplayer(object):
    def __init__(self):
        self._window_created = False
        self._aspect_ratio = 1.0
        self._observation_size = 84  # 84x84
        self._observation_display_scale = 4 # scale up by 4
        self._window_name = "image"
        self._key_mapping = {
            ord('i'): UserInput.FORWARD,
            ord("j"): UserInput.LEFT,
            ord("k"): UserInput.BACK,
            ord("l"): UserInput.RIGHT,
            ord(" "): UserInput.PICKUP,
            ord("q"): UserInput.QUIT            
        }

    def create_window(self):
        if self._window_created:
            return
        # find the aspect ratio for the screen by creating a test window
        cv2.namedWindow("test", cv2.WINDOW_NORMAL)
        x,y,width,height=cv2.getWindowImageRect("test")
        self._aspect_ratio = float(width)/float(height)
        cv2.destroyWindow("test")
        # now create the actual display window
        cv2.namedWindow(self._window_name, cv2.WINDOW_NORMAL) # cv2.WINDOW_AUTOSIZE, WINDOW_NORMAL
        rescaled_width = int(float(self._observation_size * self._observation_display_scale) * self._aspect_ratio)
        rescaled_height = int(self._observation_size * self._observation_display_scale)
        cv2.resizeWindow(self._window_name, rescaled_width, rescaled_height)
        self._window_created = True

    def destroy_window(self):
        if self._window_created:
            cv2.destroyWindow(self._window_name)
            self._window_created = False

    def update_image(self, bgr_image):
        # image is a numpy array with shape (84,84,3), with BGR ordering
        if self._window_created:
            cv2.imshow(self._window_name, bgr_image)
        else:
            raise RuntimeError("update_image: window not initialized")

    def scan_for_input(self):
        key = cv2.waitKey(10)
        val = self._key_mapping.get(key, None)
        return val



class L2ExplorerGUIAgent(object):
    def __init__(self, env:L2ExplorerTask, param_gui:ParameterGui, image_display:CV2ImageDisplayer, params={}):
        self._env = env
        self._param_gui = param_gui
        self._params = params
        self._image_display = image_display
        self._image_display.create_window()
        self._image_index = ImageType.RGB_IMAGE.value
        self._do_quit = False
        self._do_reset = False
        self._param_gui.set_agent(self)

    def reset_env(self, params):
        self._params.update(params)        
        self._do_reset = True

    def quit_env(self):
        self._do_quit = True

    def set_image_type(self, image_type:ImageType):
        self._image_index = image_type.value

    def run(self, max_steps):
        self._image_display.create_window()        
        try:
            done, num_steps = False, 0
            self._do_reset = True
            while not (done or self._do_quit) and num_steps < max_steps:
                if self._do_reset:
                    print("L2Explorer GUI Agent: Sending RESET")
                    self._do_reset = False
                    state = self._env.reset(self._params)
                    reward, done, info = 0, False, None
                    linear_velocity, angular_velocity, do_pickup = 0, 0, 0

                npstate = np.array(state['visual']) # shape is (3,1,84,84,3) RGB ordering
                rgb_img = npstate[1, :, :, :]
                bgr_img = rgb_img[:, :, [2,1,0]]
                self._image_display.update_image(bgr_img)

                # Units 
                #   linear velocity: meters per sec
                #   angular velocity: degrees per second
                do_pickup = 0
                key = self._image_display.scan_for_input()
                if key == UserInput.LEFT:
                    angular_velocity = angular_velocity - 2
                elif key == UserInput.RIGHT:
                    angular_velocity = angular_velocity + 2
                elif key == UserInput.FORWARD:
                    linear_velocity = linear_velocity + 0.3
                elif key == UserInput.BACK:
                    linear_velocity = linear_velocity - 0.3
                elif key == UserInput.PICKUP:
                    do_pickup = 1
                elif key == UserInput.QUIT:
                    self._do_quit = True

                action = [linear_velocity, angular_velocity, do_pickup]                
                state, reward, done, info = self._env.step(action)

                self._param_gui.update_action_value(action)
                self._param_gui.process_events()
                num_steps += 1
        finally:
            if done:
                print("L2Explorer GUI Agent: DONE")
            elif self._do_quit:
                print("L2Explorer GUI Agent: QUIT")
            else:
                print("L2Explorer GUI Agent: Exceeded maxsteps = {0}".format(max_steps))
                
            self._image_display.destroy_window()
            self._param_gui.close()
            self._env.close_env()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GUI agent for L2Explorer")
    parser.add_argument('-maxsteps', type=int, default=1000, help="Max number of time steps (def=1000). Set to 0 to disable.")
    parser.add_argument('-jsonfile', type=str, help="File to environment JSON.")
    args = parser.parse_args()

    #load param
    with open(args.jsonfile) as json_file:
        parsed_json = json.load(json_file)

    max_steps = sys.maxsize if args.maxsteps == 0 else args.maxsteps    

    print("""
    To move the agent, click on the image window, and use ijkl keys.
              i  (forward)
    j (left)                  l (right)
              k (back)
    ---
    <space> to pickup.
    """)

    param_gui = ParameterGui.make_gui()
    l2ex_env = L2ExplorerTask()
    image_display = CV2ImageDisplayer()
    agent = L2ExplorerGUIAgent(l2ex_env, param_gui=param_gui, image_display=image_display, params=parsed_json)
    agent.run(max_steps=max_steps)

