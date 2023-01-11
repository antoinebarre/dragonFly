"""SUBMODULE GEOGRAPHY
    This module contains all the geographic utilities for the DragonFlly application


LIST OF CLASSES:
    - Position : geographic position classes
"""

#MODULES IMPORT
from dataclasses import dataclass


@dataclass
class Possition:
    """Class for the management of ECEF position
    """
    x: float
    y: float
    z: float

    pass

