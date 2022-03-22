from typing import Any, Dict

from ml_collections import config_dict
from meltingpot.python.utils.substrates import colors
from meltingpot.python.utils.substrates import game_object_utils
from meltingpot.python.utils.substrates import shapes

PrefabConfig = game_object_utils.PrefabConfig

DEFAULT_ASCII_MAP = """
WWWWWWWWWWWWWWWWWWWWWWWWW
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
W,,,,,,,,,,,,,,,,,,,,,,,W
WWWWWWWWWWWWWWWWWWWWWWWWW
"""

CHAR_PREFAB_MAP = {
    "W": "wall",
    ",": "ground"
}

BLACK = (0,0,0,255)
SOFT_BLACK = (36,36,36,255)
GREY = (84,84,84,255)
SOFT_GREY = (120,120,120,255)

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
        {"component": "Transform",},
        {
            "component": "Appearance",
            "kwargs": {
                "renderMode": "ascii_shape",
                "spriteNames": ["Wall",],
                "spriteShapes": [shapes.WALL],
                "palettes": [{"*": (95, 95, 95, 255),
                              "&": (100, 100, 100, 255),
                              "@": (109, 109, 109, 255),
                              "#": (152, 152, 152, 255)}],
                "noRotates": [True]
            }
        },
        {
            "component": "AllBeamBlocker",
            "kwargs": {}
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

PREFABS = {
    "wall": WALL,
    "ground": create_ground_prefab(),
}