# l2explorer_env Changelog

All notable changes to this repository are documented here. We are using [Semantic Versioning for Documents](https://semverdoc.org/), in which a version number has the format `major.minor.patch`.

## 1.0.0

Updates to baseline agents and curricula for release

## 9.1.1

Updates to curriculum execution, inclusion of baselines. 

## 0.9.1 - 2021-7-13

Minor updates on documentation, unit8 support for images, bug fixes. Compatible with l2explorer049.

## 0.9.0 - 2021-1-20

Minor updates on documentation, spawning agent. Compatible with l2explorer047.

## 0.8.0 - 2020-12-20

Changes for split assets with l2explorer 047.

## 0.7.0 - 2020-11-09

Major changes for compatibility with L2explorer 045. This includes modifications to the side channels to support object creation, support for new modes of object interaction, and additional examples. A logging example is also provided with this version.

## 0.6.0 - 2020-08-08

Major changes to incorporate latest version of MLAgents (and use of side channel implementation)
Bug fixes and code refactoring

## 0.5.2 - 2020-03-06

- Updated documentation (docs/Outline.md) with defaults for spawnable objects
- Bug fixes

## 0.5.1 - 2020-01-25

- Updated examples and descriptions in docs/Outline.md
- Minor fixes to JSON templates for procedural generation

## 0.5.0 - 2019-12-05

Major revamp of design

- Support for procedurally generated environments in L2Explorer application
  - The `reset()` method takes a Python dict with a rich set of capabilities ([more info](docs/Outline.md))
- Procedural generation of stochastically co-occurring objects (`l2explorer/l2procgen/`)
- GUI agent that allows a human to play the part of the AI agent (`examples/l2ex_guiagent`)
- Tested + supported on Linux

## 0.1.0 - 2019-09-01

- Initial submission
- Support for parameterized L2Explorer tasks
- Singleton implementation, so that the Unity executable isn't reloaded for each task
- Tested on Windows and Linux
