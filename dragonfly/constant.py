"""Store all the constant used by dragonFly
"""

# IMPORTED MODULES
import math


#############################################  EARTH MODELS  #############################################

_ELLIPSOID = ["WGS84"]

_ELLIPSOID_PARAMETER =[
    {"name":"WGS84","semiMajorAxis":  6378137.0,"inverseFlattening": 298.257223563 }
]


class EarthModel():
   
    def __init__(self,model) -> None:
        self.model = model.upper()
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if value.upper() in _ELLIPSOID:
            self._model=value.upper()
        else:
            raise ValueError(f"the model {value.upper()} is not in the list of available ellipsoid models (ie. {_ELLIPSOID})")
        
    @property
    def a(self):
        """_semi major axis value of the ellispoid in meters
        """
        model_dict = next(item for item in _ELLIPSOID_PARAMETER if item["name"] == self.model)
        return model_dict["semiMajorAxis"]
    @property
    def f(self):
        "flattening of the ellispoid"
        model_dict = next(item for item in _ELLIPSOID_PARAMETER if item["name"] == self.model)
        return 1/model_dict["inverseFlattening"]
    
    @property
    def b(self):
        """Semi minor acis of the ellispoid in meters"""
        return   (1-self.f)*self.a
    
    @property
    def e(self):
        """Excentricity of the ellispoid"""
        return math.sqrt((self.a**2-self.b**2)/self.a**2)
    

        
