"""Store all the constant used by dragonFly
"""

# IMPORTED MODULES
import math

# ------------------------  EARTH MODELS  ------------------------

_ELLIPSOID = ["WGS84", "SPHERICAL"]

# List of available Ellipsoid
_ELLIPSOID_PARAMETER = [
    {"name": "WGS84", "semiMajorAxis": 6378137.0,
     "flattening": 1/298.257223563, "J2": 1.08263E-3},
    {"name": "SPHERICAL", "semiMajorAxis": 6378137.0,
     "flattening": 0, "J2": 0}
]

# default ellipsoid model
_DEFAULT_MODEL = "WGS84"

# -------------------------------------------------------------------
#                       FOLDER ANALYSIS
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

        if value in _ELLIPSOID:
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
        model_dict = next(item for item in _ELLIPSOID_PARAMETER
                          if item["name"] == self.model)
        return model_dict["semiMajorAxis"]

    @property
    def f(self) -> float:
        """flattening of the ellispoid

        Returns:
            float: flattening of the ellispoid
        """
        model_dict = next(item for item in _ELLIPSOID_PARAMETER
                          if item["name"] == self.model)
        return model_dict["flattening"]

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
        model_dict = next(item for item in _ELLIPSOID_PARAMETER
                          if item["name"] == self.model)
        return model_dict["J2"]

# ----------------------  VISUAL FRAMEWORK  -------------------


LINE_SIZE = 78
