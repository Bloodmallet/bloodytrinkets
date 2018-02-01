Bloodytrinkets
===========

> Automatation tool to calculate the worth of all dps trinkets of all classes in World of Warcraft using SimulationCraft.

## Requirements
You need a working SimulationCraft version, Python 3.5 or newer and the module [simc_support](https://github.com/Bloodmallet/simc_support) which is handled in the requirements.txt.

## Download
Download or clone this repository into your SimulationCraft directory. `simulationcraft\bloodytrinkets`

## Setup
Start your python environement. Install dependencies.
```sh
$ <env_name>\Scripts\active
(<env_name>)$ pip install -U -r .\requirements.txt
```

`pip freeze` should return something like this: "-e git+https://github.com/Bloodmallet/simc_support.git@e806d5ca289072684c6aca5fb03ce2b44e88cc4e#egg=simc_support"

## Getting started
Edit settings.py to your liking using any text editor. Start your python environement. Start bloodytrinkets.
```sh
$ <env_name>\Scripts\active
(<env_name>)$ python .\bloodytrinkets.py
```

## Development
You can start right away. The strongest need right now would probably be the implementation of tests. But as I want to merge my different projects into one with the coming Battle for Azeroth expansion, be prepared, that those are probably going to see heavy changes. Anyway, I'd love to help if someone is interested in improving or adding something.
