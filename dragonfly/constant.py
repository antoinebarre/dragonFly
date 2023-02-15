"""Store all the constants used by dragonFly
"""

# IMPORTED MODULES
import math
from collections import namedtuple

__all__ = ["EarthModel"]

# ------------------------  GLOBAL NAMETUPLE  ------------------------

_Ellipsoid_parameters = namedtuple("_Ellipsoid_parameters", (
    "name",
    "semiMajorAxis",
    "flattening",
    "j2",
))

# ------------------------  EARTH MODELS  ------------------------

# default ellipsoid model
_DEFAULT_MODEL = "WGS84"

_ELLIPSOIDS = [
    _Ellipsoid_parameters(
        name="WGS84",
        semiMajorAxis=6378137.0,
        flattening=1/298.257223563,
        j2=1.08263E-3,
    ),
    _Ellipsoid_parameters(
        name="SPHERICAL",
        semiMajorAxis=6378137.0,
        flattening=0.0,
        j2=0.0,
    )
]

# -------------------------------------------------------------------
#                       EARTH MODEL
# -------------------------------------------------------------------


class EarthModel():

    earthRotationRate = 72.92115E-6  # rotation rate from the WGS84 rad/s
    mu = 3.986004418E14  # m-3s-2

    # ---------------------- CREATOR ------------------------

    def __init__(self, model: str = _DEFAULT_MODEL) -> None:
        """Create Earth Model Object

        Args:
            model (str, optional): ellipsoid model name. Defaults to WGS84.
        """
        try:
            model = model.upper()
        except Exception:
            msg = f"the model value {model} is not an appropriate string"
            raise AttributeError(msg)
        self.model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        """ Check the setter for the model"""
        try:
            value = value.upper()
        except Exception:
            msg = f"the model value {value} is not an appropriate string"
            raise AttributeError(msg)

        if value in [ellipsoid.name for ellipsoid in _ELLIPSOIDS]:
            self._model = value.upper()
        else:
            msg = (f"the model {value.upper()}"
                   " is not in the list of available ellipsoid models"
                   "(ie. {_ELLIPSOID})"
                   )
            raise AttributeError(msg)

    # --------------------- PROPERTIES
    @property
    def a(self) -> float:
        """semi major axis value of the ellispoid in meters

        Returns:
            float: semi major axis value of the ellispoid in meters
        """
        model = next(item for item in _ELLIPSOIDS
                     if item.name == self.model)
        return model.semiMajorAxis

    @property
    def f(self) -> float:
        """flattening of the ellispoid

        Returns:
            float: flattening of the ellispoid
        """
        model = next(item for item in _ELLIPSOIDS
                     if item.name == self.model)
        return model.flattening

    @property
    def b(self) -> float:
        """Semi minor acis of the ellispoid in meters

        Returns:
            float: Semi minor acis of the ellispoid in meters
        """
        return (1-self.f)*self.a

    @property
    def e(self) -> float:
        """Excentricity of the ellispoid

        Returns:
            float: Excentricity of the ellispoid
        """
        return math.sqrt((self.a**2-self.b**2)/self.a**2)

    @property
    def j2(self) -> float:
        """Second gravitationla constant

        Returns:
            float: Second gravitationla constant
        """
        model = next(item for item in _ELLIPSOIDS
                     if item.name == self.model)
        return model.j2

# ----------------------  VISUAL FRAMEWORK  -------------------


LINE_SIZE = 78
