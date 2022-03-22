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
                "spriteNames": ["Avatar"],
                "spriteRGBColors": [(0, 0, 128)],
                "palettes": [{}],  # Will be overridden.
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
          "map": " _ ",
          "prefabs": {
              "avatar": AVATAR,
              "spawn_point": SPAWN_POINT,
            },
          "charPrefabMap": {"_": "spawn_point"},
          "playerPalettes": [],
      },
  }

  return config
