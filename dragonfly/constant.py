"""Store all the constant used by dragonFly
"""

# IMPORTED MODULES
import math


#############################################  EARTH MODELS  #############################################

_ELLIPSOID = ["WGS84","SPHERICAL"]

_ELLIPSOID_PARAMETER =[
    {"name":"WGS84","semiMajorAxis":  6378137.0,"flattening": 1/298.257223563,"j2":1.08263E-3},
    {"name":"SPHERICAL","semiMajorAxis":  6378137.0,"flattening": 0,"J2":0}
]

_DEFAULT_MODEL = "WGS84"

class EarthModel():

    earthRotationRate = 72.92115E-6 #rotation rate from the WGS84 rad/s
    mu = 3.986004418E14 #m-3s-2
   
    def __init__(self,model=_DEFAULT_MODEL) -> None:
        self.model = model.upper()
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        try:
            value = value.upper()
        except:
            raise TypeError(f"the model value {value} is not an appropriate string")
        
        if value in _ELLIPSOID:
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
        return model_dict["flattening"]
    
    @property
    def b(self):
        """Semi minor acis of the ellispoid in meters"""
        return   (1-self.f)*self.a
    
    @property
    def e(self):
        """Excentricity of the ellispoid"""
        return math.sqrt((self.a**2-self.b**2)/self.a**2)

    @property
    def j2(self):
        "Second gravitationla constant"
        model_dict = next(item for item in _ELLIPSOID_PARAMETER if item["name"] == self.model)
        return model_dict["j2"]
    

        
