# Copyright 2020 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Configuration for tutorial level: Harvest."""

from ml_collections import config_dict
from meltingpot.python.utils.substrates import shapes

BLACK = (0,0,0,255)
SOFT_BLACK = (36,36,36,255)
GREY = (84,84,84,255)
SOFT_GREY = (120,120,120,255)

#we need the spawn point in order to to see the avatars in action
SPAWN_POINT = {
    "name": "spawn_point",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState": "spawnPoint",
                "stateConfigs": [{
                    "state": "spawnPoint",
                    "groups": ["spawnPoints"],
                }],
            }
        },
        {
            "component": "Transform",
        },
    ]
}

AVATAR = {
    "name": "avatar",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState": "player",
                "stateConfigs": [
                    {"state": "player",
                     "layer": "upperPhysical",
                     "sprite": "Avatar",},
                ]
            }
        },
        {
            "component": "Transform",
        },
        {
            "component": "Appearance",
            "kwargs": {
                "renderMode": "ascii_shape",
                "spriteNames": ["Avatar"],
                "spriteShapes": [shapes.CUTE_AVATAR],
                #"spriteRGBColors": [(0, 0, 128)],
                "palettes": [{}],  # Will be overridden.
                "noRotates": [True],
            }
        },
        {
            "component": "Avatar",
            "kwargs": {
                "aliveState": "player",
                "waitState": "playerWait",
                "spawnGroup": "spawnPoints",
                "view": {
                    "left": 3,
                    "right": 3,
                    "forward": 5,
                    "backward": 1,
                    "centered": False,
                }
            }
        },
    ]
}

WALL = {
    "name": "wall",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState": "wall",
                "stateConfigs": [{
                    "state": "wall",
                    "layer": "upperPhysical",
                    "sprite": "Wall",
                }],
            }
        },
        {
            "component": "Transform",
        },
        {
            "component": "Appearance",
            "kwargs": {
                "renderMode": "ascii_shape",
                "spriteNames": ["Wall",],
                "spriteShapes": [shapes.WALL],
                "palettes": [shapes.WALL_PALETTE],
                "noRotates": [True],
            }
        },
        {
            "component": "BeamBlocker",
            "kwargs": {
                "beamType": "gift"
            }
        },
        {
            "component": "BeamBlocker",
            "kwargs": {
                "beamType": "zap"
            }
        },
    ]
}

def create_ground_prefab():
    """Return a prefab for a colorable ground prefab."""
    
    names = ["BlackGround", "SoftBlackGround", "GreyGround", "SoftGreyGround"]
    colors = [BLACK, SOFT_BLACK, GREY, SOFT_GREY]
    
    prefab = {
        "name": "ground",
        "components": [
            {
               "component" : "StateManager",
               "kwargs": {
                   "initialState": "clean",
                   "stateConfigs": [
                       {
                         "state": "clean",
                         "layer": "alternateLogic", #(understand better the meaning)
                       },
                       {
                         "state": "black",
                         "layer": "alternateLogic", #(understand better the meaning)
                         "color": names[0], 
                       },
                       {
                         "state": "softBlack",
                         "layer": "alternateLogic", #(understand better the meaning)
                         "color": names[1], 
                       },
                       {
                         "state": "grey",
                         "layer": "alternateLogic", #(understand better the meaning)
                         "color": names[2], 
                       },
                       {
                         "state": "softGrey",
                         "layer": "alternateLogic", #(understand better the meaning)
                         "color": names[3], 
                       },
                   ]
                  
               } 
            },
            {"component": "Transform",},
            {
                "component": "Appearance",
                "kwargs":{
                    "names": names,
                    "RGBColors": colors
                }
            },
            {
                "component": "Ground",
                "kwargs": {
                    "teamNames": ["black", "softBlack", "grey", "softGrey"],
                }
            },
        ]
    }
    return prefab 

def get_config():
  """Default configuration for the Harvest level."""
  config = config_dict.ConfigDict()

  # Basic configuration.
  config.individual_observation_names = ["RGB"]
  config.global_observation_names = ["WORLD.RGB"]

  # Lua script configuration.
  config.lab2d_settings = {
      "levelName": #
          "harvest",
      "levelDirectory":
          "examples//tutorial/harvest_stella/levels",
      "maxEpisodeLengthFrames":
          100,
      "numPlayers":
          1,
      "spriteSize":
          8,
      "simulation": {
          "map": """ 
          *******
          *,,,,,*
          *  _  *
          *,,,,,*
          *,,,,,*
          *******
          """,
          "prefabs": {
              "avatar": AVATAR,
              "spawn_point": SPAWN_POINT,
              "wall": WALL,
              ",": create_ground_prefab()
            },
          "charPrefabMap": {"_": "spawn_point", "*": "wall", ",": "ground"},
          "playerPalettes": [],
      },
  }

  return config
