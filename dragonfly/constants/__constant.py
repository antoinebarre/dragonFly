"""Store all the constants used by dragonFly
"""

__all__ = [
    "VISUAL_FRAMEWORK"
]

# IMPORT PACKAGE
from collections import namedtuple


# ----------------------  VISUAL FRAMEWORK  -------------------

VisualFramework = namedtuple(
    typename="VisualFrameWork",
    field_names=[
        "line_size",  # size of an entire line in the console
    ],
)

VISUAL_FRAMEWORK = VisualFramework(
    line_size=78
)
