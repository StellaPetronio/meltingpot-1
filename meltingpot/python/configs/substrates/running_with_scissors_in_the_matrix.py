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
"""Configuration for Running with Scissors in the Matrix.

Example video: https://youtu.be/oqYd4Ib5g70

Players can move around the map and collect resources of `K` discrete types. In
addition to movement, the agents have an action to fire an "interaction" beam.
All players carry an inventory with the count of resources picked up since last
respawn.

Players can observe their own inventory but not the inventories of their
coplayers. When another agent is zapped with the interaction beam, an
interaction occurs. The resolution of the interactions is determined by a
traditional matrix game, where there is a `K x K` payoff matrix describing the
reward produced by the pure strategies available to the two players. The
resources map one-to-one to the pure strategies of the matrix game. Unless
stated otherwise, for the purposes of resolving the interaction, the zapping
agent is considered the row player, and the zapped agent the column player. The
actual strategy played depends on the resources picked up before the
interaction. The more resources of a given type an agent picks up, the more
committed the agent becomes to the pure strategy corresponding to that resource.

In the case of running with scissors, `K = 3`, corresponding to rock, paper, and
scissors pure strategies respectively.

The payoff matrix is the traditional rock-paper-scissors game matrix.

Running with scissors was first described in Vezhnevets et al. (2020). Two
players gather rock, paper or scissor resources in the environment and can
challenge one another to a 'rock, paper scissor' game, the outcome of which
depends on the resources they collected. It is possible to observe the policy
that one's partner is starting to implement, either by watching them pick up
resources or by noting which resources are missing, and then take
countermeasures. This induces a wealth of possible feinting strategies.

Players can also zap resources with their interaction beam to destroy them. This
creates additional scope for feinting strategies.

Players have a `5 x 5` observation window.

Vezhnevets, A., Wu, Y., Eckstein, M., Leblond, R. and Leibo, J.Z., 2020. OPtions
as REsponses: Grounding behavioural hierarchies in multi-agent reinforcement
learning. In International Conference on Machine Learning (pp. 9733-9742). PMLR.
"""

from typing import Any, Dict, List, Tuple

from ml_collections import config_dict

from meltingpot.python.utils.substrates import colors
from meltingpot.python.utils.substrates import shapes

# The number of resources must match the (square) size of the matrix.
NUM_RESOURCES = 3

# This color is yellow.
RESOURCE1_COLOR = (255, 227, 11, 255)
RESOURCE1_HIGHLIGHT_COLOR = (255, 214, 91, 255)
RESOURCE1_COLOR_DATA = (RESOURCE1_COLOR, RESOURCE1_HIGHLIGHT_COLOR)
# This color is violet.
RESOURCE2_COLOR = (109, 42, 255, 255)
RESOURCE2_HIGHLIGHT_COLOR = (132, 91, 255, 255)
RESOURCE2_COLOR_DATA = (RESOURCE2_COLOR, RESOURCE2_HIGHLIGHT_COLOR)
# This color is cyan.
RESOURCE3_COLOR = (42, 188, 255, 255)
RESOURCE3_HIGHLIGHT_COLOR = (91, 214, 255, 255)
RESOURCE3_COLOR_DATA = (RESOURCE3_COLOR, RESOURCE3_HIGHLIGHT_COLOR)

DEFAULT_ASCII_MAP = """
WWWWWWWWWWWWWWWWWWWWWWW
WP r  r  a   a  p  p PW
W                     W
WP r  r  a   a  p  p PW
W                     W
WP r  r  a   a  p  p PW
W                     W
W     P    P    P     W
W                     W
WP s  s  a   a  a  a PW
W                     W
WP s  s  a   a  a  a PW
W                     W
WP s  s  a   a  a  a PW
WWWWWWWWWWWWWWWWWWWWWWW
"""

_resource_names = [
    "resource_class1",
    "resource_class2",
    "resource_class3",
]

# `prefab` determines which prefab game object to use for each `char` in the
# ascii map.
CHAR_PREFAB_MAP = {
    "a": {"type": "choice", "list": _resource_names},
    "r": _resource_names[0],
    "p": _resource_names[1],
    "s": _resource_names[2],
    "P": "spawn_point",
    "W": "wall",
}

_COMPASS = ["N", "E", "S", "W"]

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
            "kwargs": {
                "position": (0, 0),
                "orientation": "N"
            }
        },
        {
            "component": "Appearance",
            "kwargs": {
                "renderMode": "ascii_shape",
                "spriteNames": ["Wall"],
                "spriteShapes": [shapes.WALL],
                "palettes": [{"*": (95, 95, 95, 255),
                              "&": (100, 100, 100, 255),
                              "@": (109, 109, 109, 255),
                              "#": (152, 152, 152, 255)}],
                "noRotates": [False]
            }
        },
        {
            "component": "BeamBlocker",
            "kwargs": {
                "beamType": "gameInteraction"
            }
        },
    ]
}

SPAWN_POINT = {
    "name": "spawnPoint",
    "components": [
        {
            "component": "StateManager",
            "kwargs": {
                "initialState": "spawnPoint",
                "stateConfigs": [{
                    "state": "spawnPoint",
                    "layer": "alternateLogic",
                    "groups": ["spawnPoints"]
                }],
            }
        },
        {
            "component": "Transform",
            "kwargs": {
                "position": (0, 0),
                "orientation": "N"
            }
        },
    ]
}

# PLAYER_COLOR_PALETTES is a list with each entry specifying the color to use
# for the player at the corresponding index.
NUM_PLAYERS_UPPER_BOUND = 8
PLAYER_COLOR_PALETTES = []
for idx in range(NUM_PLAYERS_UPPER_BOUND):
  PLAYER_COLOR_PALETTES.append(shapes.get_palette(colors.palette[idx]))

# Primitive action components.
# pylint: disable=bad-whitespace
# pyformat: disable
NOOP       = {"move": 0, "turn":  0, "interact": 0}
FORWARD    = {"move": 1, "turn":  0, "interact": 0}
STEP_RIGHT = {"move": 2, "turn":  0, "interact": 0}
BACKWARD   = {"move": 3, "turn":  0, "interact": 0}
STEP_LEFT  = {"move": 4, "turn":  0, "interact": 0}
TURN_LEFT  = {"move": 0, "turn": -1, "interact": 0}
TURN_RIGHT = {"move": 0, "turn":  1, "interact": 0}
INTERACT   = {"move": 0, "turn":  0, "interact": 1}
# pyformat: enable
# pylint: enable=bad-whitespace

ACTION_SET = (
    NOOP,
    FORWARD,
    BACKWARD,
    STEP_LEFT,
    STEP_RIGHT,
    TURN_LEFT,
    TURN_RIGHT,
    INTERACT,
)

TARGET_SPRITE_SELF = {
    "name": "Self",
    "shape": shapes.CUTE_AVATAR,
    "palette": shapes.get_palette((50, 100, 200)),
    "noRotate": True,
}

TARGET_SPRITE_OTHER = {
    "name": "Other",
    "shape": shapes.CUTE_AVATAR,
    "palette": shapes.get_palette((200, 100, 50)),
    "noRotate": True,
}


def create_scene():
  """Creates the global scene."""
  scene = {
      "name": "scene",
      "components": [
          {
              "component": "StateManager",
              "kwargs": {
                  "initialState": "scene",
                  "stateConfigs": [{
                      "state": "scene",
                  }],
              }
          },
          {
              "component": "Transform",
              "kwargs": {
                  "position": (0, 0),
                  "orientation": "N"
              },
          },
          {
              "component": "TheMatrix",
              "kwargs": {
                  "matrix": [
                      [0, -1, 1],
                      [1, 0, -1],
                      [-1, 1, 0]
                  ],
              }
          },
      ]
  }
  return scene


def create_resource_prefab(
    resource_id: int,
    resource_shape: str,
    resource_palette: Dict[str, Tuple[int, int, int, int]]):
  """Creates resource prefab with provided resource_id, shape, and palette."""
  resource_name = "resource_class{}".format(resource_id)
  resource_prefab = {
      "name": resource_name,
      "components": [
          {
              "component": "StateManager",
              "kwargs": {
                  "initialState": resource_name,
                  "stateConfigs": [
                      {"state": resource_name + "_wait",
                       "groups": ["resourceWaits"]},
                      {"state": resource_name,
                       "layer": "lowerPhysical",
                       "sprite": resource_name + "_sprite"},
                  ]
              },
          },
          {
              "component": "Transform",
              "kwargs": {
                  "position": (0, 0),
                  "orientation": "N"
              },
          },
          {
              "component": "Appearance",
              "kwargs": {
                  "renderMode": "ascii_shape",
                  "spriteNames": [resource_name + "_sprite"],
                  "spriteShapes": [resource_shape],
                  "palettes": [resource_palette],
                  "noRotates": [True]
              },
          },
          {
              "component": "Resource",
              "kwargs": {
                  "resourceClass": resource_id,
                  "visibleType": resource_name,
                  "waitState": resource_name + "_wait",
                  "groupToRespawn": "resourceWaits",
                  "regenerationRate": 0,
                  "regenerationDelay": 1000
              },
          },
          {
              "component": "Destroyable",
              "kwargs": {
                  "visibleType": resource_name,
                  "waitState": resource_name + "_wait",
                  "initialHealth": 2,
              },
          },
      ]
  }
  return resource_prefab


def create_avatar_object(player_idx: int,
                         all_source_sprite_names: List[str],
                         target_sprite_self: Dict[str, Any],
                         target_sprite_other: Dict[str, Any]) -> Dict[str, Any]:
  """Create an avatar object given self vs other sprite data."""
  # Lua is 1-indexed.
  lua_index = player_idx + 1

  # Setup the self vs other sprite mapping.
  source_sprite_self = "Avatar" + str(lua_index)
  custom_sprite_map = {source_sprite_self: target_sprite_self["name"]}
  for name in all_source_sprite_names:
    if name != source_sprite_self:
      custom_sprite_map[name] = target_sprite_other["name"]

  live_state_name = "player{}".format(lua_index)
  avatar_object = {
      "name": "avatar",
      "components": [
          {
              "component": "StateManager",
              "kwargs": {
                  "initialState": live_state_name,
                  "stateConfigs": [
                      {"state": live_state_name,
                       "layer": "upperPhysical",
                       "sprite": source_sprite_self,
                       "contact": "avatar",
                       "groups": ["players"]},

                      {"state": "playerWait",
                       "groups": ["playerWaits"]},
                  ]
              }
          },
          {
              "component": "Transform",
              "kwargs": {
                  "position": (0, 0),
                  "orientation": "N"
              }
          },
          {
              "component": "Appearance",
              "kwargs": {
                  "renderMode": "colored_square",
                  "spriteNames": [source_sprite_self],
                  # A white square should never be displayed. It will always be
                  # remapped since this is self vs other observation mode.
                  "spriteRGBColors": [(255, 255, 255, 255)],
              }
          },
          {
              "component": "AdditionalSprites",
              "kwargs": {
                  "renderMode": "ascii_shape",
                  "customSpriteNames": [target_sprite_self["name"],
                                        target_sprite_other["name"]],
                  "customSpriteShapes": [target_sprite_self["shape"],
                                         target_sprite_other["shape"]],
                  "customPalettes": [target_sprite_self["palette"],
                                     target_sprite_other["palette"]],
                  "customNoRotates": [target_sprite_self["noRotate"],
                                      target_sprite_other["noRotate"]],
              }
          },
          {
              "component": "Avatar",
              "kwargs": {
                  "index": lua_index,
                  "aliveState": live_state_name,
                  "waitState": "playerWait",
                  "speed": 1.0,
                  "spawnGroup": "spawnPoints",
                  "actionOrder": ["move", "turn", "interact"],
                  "actionSpec": {
                      "move": {"default": 0, "min": 0, "max": len(_COMPASS)},
                      "turn": {"default": 0, "min": -1, "max": 1},
                      "interact": {"default": 0, "min": 0, "max": 1},
                  },
                  "view": {
                      "left": 2,
                      "right": 2,
                      "forward": 3,
                      "backward": 1,
                      "centered": False
                  },
                  "spriteMap": custom_sprite_map,
                  # The following kwarg makes it possible to get rewarded even
                  # on frames when an avatar is "dead". It is needed for in the
                  # matrix games in order to correctly handle the case of two
                  # players getting hit simultaneously by the same beam.
                  "skipWaitStateRewards": False,
              }
          },
          {
              "component": "GameInteractionZapper",
              "kwargs": {
                  "cooldownTime": 2,
                  "beamLength": 3,
                  "beamRadius": 1,
                  "framesTillRespawn": 1000,
                  "numResources": NUM_RESOURCES,
                  "endEpisodeOnFirstInteraction": True,
              }
          },
          {
              "component": "ReadyToShootObservation",
              "kwargs": {
                  "zapperComponent": "GameInteractionZapper",
              }
          },
          {
              "component": "InventoryObserver",
              "kwargs": {
              }
          },
          {
              "component": "Taste",
              "kwargs": {
                  "mostTastyResourceClass": -1,  # -1 indicates no preference.
                  # No resource is most tasty when mostTastyResourceClass == 1.
                  "mostTastyReward": 0.1,
              }
          },
          {
              "component": "InteractionTaste",
              "kwargs": {
                  "mostTastyResourceClass": -1,  # -1 indicates no preference.
                  "zeroDefaultInteractionReward": False,
                  "extraReward": 1.0,
              }
          },
          {
              "component": "LocationObserver",
              "kwargs": {
                  "objectIsAvatar": True,
                  "alsoReportOrientation": True
              }
          },
          {
              "component": "AvatarMetricReporter",
              "kwargs": {
                  "metrics": [
                      {
                          # Report the inventories of both players involved in
                          # an interaction on this frame formatted as
                          # (self inventory, partner inventory).
                          "name": "INTERACTION_INVENTORIES",
                          "type": "tensor.DoubleTensor",
                          "shape": (2, NUM_RESOURCES),
                          "component": "GameInteractionZapper",
                          "variable": "latest_interaction_inventories",
                      },
                  ]
              }
          },
      ]
  }
  return avatar_object


def create_prefabs():
  """Returns a dictionary mapping names to template game objects."""
  prefabs = {
      "wall": WALL,
      "spawn_point": SPAWN_POINT,
  }
  prefabs["resource_class1"] = create_resource_prefab(
      1, shapes.BUTTON, {"*": RESOURCE1_COLOR_DATA[0],
                         "#": RESOURCE1_COLOR_DATA[1],
                         "x": (0, 0, 0, 0)})
  prefabs["resource_class2"] = create_resource_prefab(
      2, shapes.BUTTON, {"*": RESOURCE2_COLOR_DATA[0],
                         "#": RESOURCE2_COLOR_DATA[1],
                         "x": (0, 0, 0, 0)})
  prefabs["resource_class3"] = create_resource_prefab(
      3, shapes.BUTTON, {"*": RESOURCE3_COLOR_DATA[0],
                         "#": RESOURCE3_COLOR_DATA[1],
                         "x": (0, 0, 0, 0)})
  return prefabs


def get_all_source_sprite_names(num_players):
  all_source_sprite_names = []
  for player_idx in range(0, num_players):
    # Lua is 1-indexed.
    lua_index = player_idx + 1
    all_source_sprite_names.append("Avatar" + str(lua_index))

  return all_source_sprite_names


def create_avatar_objects(num_players):
  """Returns list of avatar objects of length 'num_players'."""
  all_source_sprite_names = get_all_source_sprite_names(num_players)
  avatar_objects = []
  for player_idx in range(0, num_players):
    game_object = create_avatar_object(player_idx,
                                       all_source_sprite_names,
                                       TARGET_SPRITE_SELF,
                                       TARGET_SPRITE_OTHER)
    avatar_objects.append(game_object)

  return avatar_objects


def create_world_sprite_map(
    num_players: int, target_sprite_other: Dict[str, Any]) -> Dict[str, str]:
  all_source_sprite_names = get_all_source_sprite_names(num_players)
  world_sprite_map = {}
  for name in all_source_sprite_names:
    world_sprite_map[name] = target_sprite_other["name"]

  return world_sprite_map


def create_lab2d_settings(num_players: int) -> Dict[str, Any]:
  """Returns the lab2d settings."""
  lab2d_settings = {
      "levelName": "the_matrix",
      "levelDirectory": "meltingpot/lua/levels",
      "numPlayers": num_players,
      "episodeLengthFrames": 1000,
      "spriteSize": 8,
      "simulation": {
          "map": DEFAULT_ASCII_MAP,
          "gameObjects": create_avatar_objects(num_players),
          "scene": create_scene(),
          "prefabs": create_prefabs(),
          "charPrefabMap": CHAR_PREFAB_MAP,
          # worldSpriteMap is needed to make the global view used in videos be
          # be informative in cases where individual avatar views have had
          # sprites remapped to one another (example: self vs other mode).
          "worldSpriteMap": create_world_sprite_map(num_players,
                                                    TARGET_SPRITE_OTHER),
      },
  }
  return lab2d_settings


def get_config():
  """Default config for training on running_with_scissors_in_the_matrix."""
  config = config_dict.ConfigDict()

  # Basic configuration.
  config.num_players = 2

  # Lua script configuration.
  config.lab2d_settings = create_lab2d_settings(config.num_players)

  # Action set configuration.
  config.action_set = ACTION_SET
  # Observation format configuration.
  config.individual_observation_names = [
      "RGB",
      "INVENTORY",
      "READY_TO_SHOOT",
      "POSITION",
      "ORIENTATION",
      "INTERACTION_INVENTORIES",
  ]
  config.global_observation_names = [
      "WORLD.RGB",
  ]

  return config
