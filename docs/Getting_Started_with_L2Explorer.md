# Getting Started with the L2Explorer Learning Environment

_Document version 1.0_

<!-- TOC -->

- [1. Get the L2Explorer Executable](#1-get-the-l2explorer-executable)
- [2. Installation for Linux](#2-installation-for-linux)
  - [2.1. Install Python](#21-install-python)
  - [2.2. Create a Python Virtual Environment](#22-create-a-python-virtual-environment)
  - [2.3. Install L2Explorer Python Libraries](#23-install-l2explorer-python-libraries)
  - [2.4. Configure Environment Variables](#24-configure-environment-variables)
  - [2.5. Test execution of a syllabus with custom reset parameters](#25-test-execution-of-a-syllabus-with-custom-reset-parameters)
- [3. Running with Docker without GPU](#3-running-with-docker-without-gpu)
- [4. Headless Linux servers with GPUs](#4-headless-linux-servers-with-gpus)
- [5. Headless Linux servers without GPUs (virtual x-frame buffer)](#5-headless-linux-servers-without-gpus-virtual-x-frame-buffer)
- [6. Troubleshooting](#6-troubleshooting)

<!-- /TOC -->

This document provides instructions on installing the L2Explorer environment for testing Continual Reinforcement Learning. This approach is built on top of the [Unity ML-Agents](https://github.com/Unity-Technologies/ml-agents) project along with custom Unity environments.

This is an early beta version of this code, and additional information on topics such as parallel execution will follow.


# 1. Get the L2Explorer Executable and Assets

In the following steps, you will be guided how to download both the executable and the assets file. The assets file contains 3D art files separately from the executable to allow for modular and efficient loading. You will then be directed to unzip the files, and note the location of the asset folder.

The L2Explorer Unity environment is provided as a pre-compiled application, currently supported on Windows (Win10) and Linux (Ubuntu 18.04).

To download the binaries, do the following:

1. TODO has links for the L2Explorer application for each platform, packaged as a zip file. Download the latest **machine-playable** version.
2. TODO has links for the L2Explorer Assets, packaged as a zip file. Download the latest version.
3. Unzip the downloaded zip file for the executable. For example, for Linux, if the zip file is `l2explorer-047-linux.zip`, it will extract to a folder with the same name, containing the executable `l2explorer.x86_64`.
4. Unzip the downloaded zip file for the assets. For example if the zip file is `l2mAssets.zip`, it will extract to a folder with the same name, containing two folders windows and linux.
5. Make a note of the full path to the executable and the l2mAssets folder. This will be needed in [2.4. Configure Environment Variables](#24-configure-environment-variables).
6. Give the executable execution permissions (e.g., `chmod +x path/to/executable`).

# 2. Installation for Linux

## 2.1. Install Python

Install Python 3.6 (Note that Unity ML-agents is incompatible with Python 3.7).

Ubuntu 18.04 with Python 3.6 is the recommended and tested configuration for L2Explorer.

If there is already a version of Python on your system, verify it by running `python --version`.

In some Ubuntu installs, both Python 2 and 3 may be installed. If your python version above reports Python 2, try `python3 --version`.

## 2.2. Create a Python Virtual Environment

Build the virtual environment (we use [venv](https://docs.python.org/3/tutorial/venv.html) that comes pre-built with Python for this guide):

For Linux:

```bash
python3.6 -m venv <path_to_new_virtual_environment>
```

Windows users may want to download anaconda (https://www.anaconda.com/products/individual), and use the anaconda terminal to create the virtual environment.

Note: for the rest of this guide, we assume the virtual environment is set as:

```bash
python3.6 -m venv ~/workspace/L2Explorer
```

Activate the virtual environment as follows.

```bash
source ~/workspace/L2Explorer/bin/activate
```

You can deactivate the virtual environment with the following command:

For Linux:

```bash
deactivate
```

## 2.3 Install Unity ML-Agents 

The release_2 (0.16.0) tag of the Unity ML Agents Python libraries needs to be installed (the customization consists of a specialized Protobuf message for encoding parameters when resetting an environment). The libraries may be installed as follows:

For Linux (from the command line run):

```bash
pip install mlagents==0.16.0
```

## 2.4. Install L2Explorer Python Libraries

Clone the `l2logger` and `l2explorer_env` repositories from the DARPA L2M Github repository, e.g.:

```bash
mkdir ~/l2m
cd ~/l2m
git clone https://github.com/darpa-l2m/l2logger.git
git clone https://github.com/darpa-l2m/l2explorer_env.git
```

Install the repositories as follows:

```bash
source ~/workspace/L2Explorer/bin/activate 
pip install -e l2logger
pip install -e l2explorer_env
```

If during installation, you see an error related to `skbuild`, run the command ` pip install --upgrade pip` before installing again to correct for a known error in the opencv install.

## 2.5. Configure Environment Variables

Before running L2Explorer code, two environment variables must be set:

- `L2EXPLORER_APP`: This is the full path including filename to your downloaded Unity executable.
- `L2EXPLORER_WORKER_ID`: This is a unique id indicating the port to use to communicate to unity. `0` is the default, but can be changed if there are any communication conflicts on the port.

Then, set the `L2EXPLORER_APP` and `L2EXPLORER_WORKER_ID` environment variables as shown below for your applicable operating system. `L2EXPLORER_APP` is the full path including filename to your downloaded unity executable. `L2EXPLORER_WORKER_ID` is a unique id indicating the port to use to communicate to unity. `0` is a good default, but can be changed if there are any communication conflicts on the port.

On Linux (Bash), the environment variables may be set as follows (be sure to include the full filename and absolute path):

```bash
export L2EXPLORER_APP="/path/to/my/executable"
export L2EXPLORER_WORKER_ID=0
```

On Windows, the environment variables may be set as follows:

```dos
set L2EXPLORER_APP=C:\\path\\to\\myexecutable.exe
set L2EXPLORER_WORKER_ID=0
```

After setting the two environment variables, the  assets location file must be configured:

- `l2explorer-config.json`: contains the path to the l2mAssets library to be used

To configure the assets library, you must provide the path to the l2mAssets folder. In the same directory as the l2explorer folder that you unzipped, you should create a file named `l2explorer-config.json` (see note below that the .json should automatically be created for you if you do not create one). This should contain a single line of the form: `{"libraryPath":"/Path/to/l2mAssets"}`.

Note: If you do not have the assets library configured on startup, you will see an error message ("CRITICAL ERROR: No Library path configured") on the unity executable. An `l2explorer-config.json` file will be generated for you in the directory of the executable to add the path to l2mAssets.

Edit `l2explorer-config.json` to set the `"libraryPath"` variable to the full path to the l2mAssets folder. The file should contain `{"libraryPath":"/path/to/folder/l2mAssets"}`

## 2.6. Test execution of L2explorer

In the `l2explorer_env` repository, change into the `examples` directory and run a random agent example for a simple map. 

```bash
cd ~/l2m/l2explorer_env/examples
python random_agent.py -jsonfile map0.json
```

# 3. Running with Docker without GPU

We have created a docker image for cross-platform unity testing. This uses the xvfb frame buffer, which is slow, and so far x-forwarding is not supported. Nevertheless, this allows running l2explorer on any system with docker-ce. Refer to [Using Docker For ML-Agents](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Using-Docker.md) for more information.

1. [Install Docker CE](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
2. Pull learnkit, l2explorer_learnkit, l2explorer_env.
3. Copy the Dockerfile to the same folder level as the repositories.
4. run 'docker build -f Dockerfile10 -t unity_test .'
5. Download the linux x86 executable as well as the l2mAsset folder, copy into the data/linux folder, and set paths correctly in the Dockerfile

# 4. Headless Linux servers with GPUs

**a. Configure Xorg**

If using Linux Server, assuming a working installation of the nvidia drivers for your system.

To use visual observations on a Linux Server (such as AWS), you will need to follow the instructions under ["Setting up X Server (optional)"](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-on-Amazon-Web-Service.md).
The Unity ML team also offers a pre-configured AMI ami-016ff5559334f8619 in the us-east-1 region.

To install Xorg please follow the link above, but here is a quick summary:

**b. Install Xorg**

```bash
$ sudo apt-get update
$ sudo apt-get install -y xserver-xorg mesa-utils
$ sudo nvidia-xconfig -a --use-display-device=None --virtual=1280x1024
```

**c. Get the BusID information**

```bash
$ nvidia-xconfig --query-gpu-info
```

**d. Find your card name**

```bash
$ cat /etc/X11/org.conf
```

Look for something like "Tesla K80"

**e. Add the BusID information to your /etc/X11/xorg.conf file**

```bash
$ sudo sed -i 's/    BoardName      "Tesla K80"/    BoardName      "Tesla K80"\n    BusID          "0:30:0"/g' /etc/X11/xorg.conf
```

and check that the BusID was successfully added to the file /etc/X11/xorg.conf

**f. Remove the Section "Files"**

In the file /etc/X11/xorg.conf file, remove two lines that contain Section "Files" and EndSection

```bash
$ sudo vim /etc/X11/xorg.conf
```

**g. Reboot**

```bash
$ sudo reboot now
```

**h. After reboot, start the X server**

```bash
$ sudo /usr/bin/X :0 &
```

Press Enter to come back to the command line.

**i. Check if Xorg process is running**

You will have a list of processes running on the GPU, Xorg should be in the list.

```bash
$ nvidia-smi
```

**j. Make the ubuntu use X Server for display**

```bash
$ export DISPLAY=:0
```

**k. Test with glxgears**

For more information on glxgears, see ftp://www.x.org/pub/X11R6.8.1/doc/glxgears.1.html.

```bash
$ glxgears
```

If Xorg is configured correctly, you should see the following message running synchronized to the vertical refresh. The framerate should be approximately the same as the monitor refresh rate.

```
137296 frames in 5.0 seconds = 27459.053 FPS
141674 frames in 5.0 seconds = 28334.779 FPS
141490 frames in 5.0 seconds = 28297.875 FPS
```

# 5. Headless Linux servers without GPUs (virtual x-frame buffer)

The virtual xframe buffer can be used to run Unity applications, as in our docker container. We have not fully tested these instructions, but this may be helpful for getting unity applications running on headless linux servers without GPUs.

Prerequisites: Ubuntu 16.04, Python 3.6.4, pip 9.0.3
Install runtime dependencies

```bash
sudo apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
		libexpat1 \
		libffi6 \
		libgdbm3 \
		libreadline6 \
		libsqlite3-0 \
		libssl1.0.0 \
	&& rm -rf /var/lib/apt/lists/*
```

```bash
sudo apt-get update && apt-get -y upgrade
```

xvfb is used to do CPU based rendering of Unity

```bash
sudo apt-get install -y xvfb
```

# 6. Troubleshooting

This is still beta, in-development software. Issues with installation and performance of the unity environment will likely arise. Common issues include communication issues (https servers, proxies), and issues with the graphics engine. We will continue to grow our FAQ, for now many of these issues are addressed in the [Unity ML-Agents FAQ](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/FAQ.md).

Common issues

- Unity Environment shows "Critical Error Message": Assure that the l2explorer-config.json file has the correct file path to l2mAssets and is in the same directory as the L2Explorer executable.
- Unity Timeout exception: This can be caused by many issues, but ensure the executable has executable privileges, the path is set correctly, and the ports are available.
- Parsing errors with l2explorer_learnkit: ensure the json extension is omitted from the command to run l2explorer_learnkit

If you are having issues working with L2Explorer and have access to an AWS account, we suggest testing on a fresh EC2 Instance to replicate any bugs you encounter.

- Login to EC2 console
- Select "Launch instance"
- Search for "ami-016ff5559334f8619" under community AMIs and select
- Select p2.xlarge (ensure you have enough storage)
- Generate a new ssh key pair or use an existing one
- Using local terminal, ssh to instance (username is ubuntu@ipaddress)
- Run nvidia-smi, get following output
  Thu Jan 2 22:19:18 2020

```bash
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 390.87                 Driver Version: 390.87                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla K80           On   | 00000000:00:1E.0 Off |                    0 |
| N/A   34C    P8    29W / 149W |      0MiB / 11441MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

- Xorg is not running, so start the server

```bash
sudo /usr/bin/X :0 &
```

- Test with nvidia-smi

```bash
Thu Jan  2 22:24:35 2020
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 390.87                 Driver Version: 390.87                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla K80           On   | 00000000:00:1E.0 Off |                    0 |
| N/A   34C    P8    29W / 149W |      9MiB / 11441MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0     15667      G   /usr/lib/xorg/Xorg                             8MiB |
+-----------------------------------------------------------------------------+
```

- Set display

```bash
export DISPLAY=:0
```

- Test with glxgears

```bash
glxgears
Running synchronized to the vertical refresh.  The framerate should be
approximately the same as the monitor refresh rate.
139563 frames in 5.0 seconds = 27912.432 FPS
143086 frames in 5.0 seconds = 28617.162 FPS
142890 frames in 5.0 seconds = 28577.994 FPS
```

- Download [l2explorer_0_2_5_linux_machine.zip](https://l2explorer-app.s3.amazonaws.com/index.html)
- scp zip file to ~/ on your AWS instance using a new terminal on the local machine
- On AWS instance, mkdir l2explorer
- cp l2explorer_0_2_5_linux_machine.zip to ~/l2explorer/
- unzip l2explorer_0_2_5_linux_machine.zip
- chmod +x l2explorer_0_2_5_linux_machine/l2explorer_0_2_5_linux_machine.x86_64 (must be executable)
- create virtual environment python -m venv l2_env
- activate virtual environment source l2_env/bin/activate
- Download the two wheels from https://github.com/darpa-l2m/ml-agents/releases/tag/l2m-mlagents-0.9.3
- scp wheels from local machine to ~/l2explorer on AWS instance
- pip install mlagents_envs-0.9.3-py3-none-any.whl (run in ~/l2explorer) on AWS instance
- pip install mlagents-0.9.3-py3-none-any.whl on AWS instance
- git clone https://github.com/darpa-l2m/learnkit.git (run in ~/l2explorer)
- git clone https://github.com/darpa-l2m/l2explorer_env.git (run in ~/l2explorer)
- git clone https://github.com/darpa-l2m/l2explorer_learnkit.git (run in ~/l2explorer)
- pip install -e learnkit/
- pip install -e l2explorer_env/
- pip install -e l2explorer_learnkit/
- export L2EXPLORER_WORKER_ID=0
- export L2EXPLORER_APP="/home/ubuntu/l2explorer/l2explorer_0_2_5_linux_machine/l2explorer_0_2_5_linux_machine.x86_64"
- cd l2explorer_learnkit/examples
- python rlsyllabus_customreset.py produces the following output (note the successful runs of each step):

```bash
Duplicate key in file '/home/ubuntu/.config/matplotlib/matplotlibrc' line #2.
Duplicate key in file '/home/ubuntu/.config/matplotlib/matplotlibrc' line #3.
Matplotlib is building the font cache using fc-list. This may take a moment.
INFO:root:Logging to: /home/ubuntu/l2data/logs
2020-01-02 22:51:12,079 <2708> [INFO    ] root - Logging to: /home/ubuntu/l2data/logs
INFO:root:Loading /home/ubuntu/l2explorer/l2explorer_learnkit/examples/rlsyllabus_test.
2020-01-02 22:51:12,079 <2708> [INFO    ] root - Loading /home/ubuntu/l2explorer/l2explorer_learnkit/examples/rlsyllabus_test.
INFO:learnkit.syllabus.syllabus:SyllabusContext:Load syllabus: "/home/ubuntu/l2explorer/l2explorer_learnkit/examples/rlsyllabus_test.json"
2020-01-02 22:51:12,125 <2708> [INFO    ] learnkit.syllabus.syllabus:SyllabusContext - Load syllabus: "/home/ubuntu/l2explorer/l2explorer_learnkit/examples/rlsyllabus_test.json"
INFO:l2explorerkit.l2explorer:FindNearbyObjects:Episode: 0 | Seed: 643148549
2020-01-02 22:51:12,126 <2708> [INFO    ] l2explorerkit.l2explorer:FindNearbyObjects - Episode: 0 | Seed: 643148549
Running l2explorerkit.l2explorer:FindNearbyObjects
Available object classes: ['agent', 'tree', 'geometric', 'icosphere', 'cube', 'nature', 'shrub', 'bag', 'barrel', 'bed', 'bench', 'building', 'car', 'chair', 'rock', 'tent', 'table', 'mushroom', 'streetsign', 'roadblock', 'fence']
object pairs: [('agent', None), ('tree', None), ('shrub', None), ('rock', None), ('barrel', None), ('mushroom', None), ('tent', None), ('building', None), ('cube', 'agent'), ('streetsign', 'building'), ('roadblock', 'building'), ('fence', 'building'), ('car', 'streetsign')]
Adding 0 points for 'agent'
Adding 20 points for 'tree'
Adding 30 points for 'shrub'
Adding 100 points for 'rock'
Adding 20 points for 'barrel'
Adding 30 points for 'mushroom'
Adding 10 points for 'tent'
Adding 10 points for 'building'
Adding 0 points for 'cube'
Adding 37 points for 'streetsign'
Adding 52 points for 'roadblock'
Adding 29 points for 'fence'
Adding 182 points for 'car'
object_type: agent locations: 0
object_type: tree locations: 20
object_type: shrub locations: 30
object_type: rock locations: 100
object_type: barrel locations: 20
object_type: mushroom locations: 30
object_type: tent locations: 10
object_type: building locations: 10
object_type: cube locations: 0
object_type: streetsign locations: 37
object_type: roadblock locations: 52
object_type: fence locations: 29
object_type: car locations: 182
Found path: /home/ubuntu/l2explorer/l2explorer_0_2_5_linux_machine/l2explorer_0_2_5_linux_machine.x86_64
ALSA lib confmisc.c:768:(parse_card) cannot find card '0'
ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
ALSA lib confmisc.c:1251:(snd_func_refer) error evaluating name
ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:4771:(snd_config_expand) Evaluate error: No such file or directory
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM default
ALSA lib confmisc.c:768:(parse_card) cannot find card '0'
ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
ALSA lib confmisc.c:1251:(snd_func_refer) error evaluating name
ALSA lib conf.c:4292:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:4771:(snd_config_expand) Evaluate error: No such file or directory
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM default
INFO:mlagents.envs:
'ML_Academy' started successfully!
Unity Academy name: ML_Academy
        Number of Brains: 1
        Number of Training Brains : 1
        Reset Parameters :
		lightColorG -> 0.800000011920929
		cZoom -> 5.0
		targetReward -> 100.0
		season -> 2.0
		cYawSubdivisions -> 24.0
		agentVisionResolution -> 3.0
		damageReward -> -50.0
		lightColorR -> 0.800000011920929
		lightIntensity -> 2.0
		agentSpeed -> 10.0
		timePenalty -> 0.0
		persistentRewardPeriod -> 30.0
		timeLimit -> 3000.0
		cVerticalSubdivisions -> 5.0
		classificationTask -> 0.0
		agentAngularSpeed -> 90.0
		agentReach -> 5.0
		lightAngle -> 50.0
		lightColorB -> 0.699999988079071
Unity brain name: L2Brain
        Number of Visual Observations (per agent): 3
        Vector Observation space size (per agent): 1
        Number of stacked Vector Observation: 1
        Vector Action space type: continuous
        Vector Action space size (per agent): [3]
        Vector Action descriptions: direction to go, rotate direction, pickup
2020-01-02 22:51:17,446 <2708> [INFO    ] mlagents.envs -
'ML_Academy' started successfully!
Unity Academy name: ML_Academy
        Number of Brains: 1
        Number of Training Brains : 1
        Reset Parameters :
		lightColorG -> 0.800000011920929
		cZoom -> 5.0
		targetReward -> 100.0
		season -> 2.0
		cYawSubdivisions -> 24.0
		agentVisionResolution -> 3.0
		damageReward -> -50.0
		lightColorR -> 0.800000011920929
		lightIntensity -> 2.0
		agentSpeed -> 10.0
		timePenalty -> 0.0
		persistentRewardPeriod -> 30.0
		timeLimit -> 3000.0
		cVerticalSubdivisions -> 5.0
		classificationTask -> 0.0
		agentAngularSpeed -> 90.0
		agentReach -> 5.0
		lightAngle -> 50.0
		lightColorB -> 0.699999988079071
Unity brain name: L2Brain
        Number of Visual Observations (per agent): 3
        Vector Observation space size (per agent): 1
        Number of stacked Vector Observation: 1
        Vector Action space type: continuous
        Vector Action space size (per agent): [3]
        Vector Action descriptions: direction to go, rotate direction, pickup
**************<learnkit.syllabus.info.Info object at 0x7f6436babba8>*******************
{}
rlsyllabus_customreset.py:64: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
  plt.show()
Episode steps: 0
Episode steps: 1
Episode steps: 2
Episode steps: 3
Episode steps: 4
Episode steps: 5
Episode steps: 6
Episode steps: 7
Episode steps: 8
Episode steps: 9
Episode steps: 10
Episode steps: 11
Episode steps: 12
Episode steps: 13
Episode steps: 14
Episode steps: 15
Episode steps: 16
Episode steps: 17
Episode steps: 18
Episode steps: 19
Episode steps: 20
Episode steps: 21
Episode steps: 22
Episode steps: 23
Episode steps: 24
Episode steps: 25
Episode steps: 26
Episode steps: 27
Episode steps: 28
Episode steps: 29
Episode steps: 30
Episode steps: 31
Episode steps: 32
Episode steps: 33
Episode steps: 34
Episode steps: 35
Episode steps: 36
Episode steps: 37
```
