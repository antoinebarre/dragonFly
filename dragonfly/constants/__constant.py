"""Store all the constants used by dragonFly
"""

__all__ = [
    "VISUAL_FRAMEWORK",
    "DEFAULT_SETTINGS",
]

# IMPORT PACKAGE
from collections import namedtuple

# ---------------------------- DEFAULT VALUE ---------------------------- #

DefaultSettings = namedtuple(
    typename="DefaultSettings",
    field_names=[
        "EarthEllipsoid",  # Name of the default ellipsoid model
    ]
)

DEFAULT_SETTINGS = DefaultSettings(
    EarthEllipsoid="WGS84",
)


# --------------------------- VISUAL FRAMEWORK -------------------------- #

VisualFramework = namedtuple(
    typename="VisualFrameWork",
    field_names=[
        "line_size",  # size of an entire line in the console
    ],
)

VISUAL_FRAMEWORK = VisualFramework(
    line_size=78
)
