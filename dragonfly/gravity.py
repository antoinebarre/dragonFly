""" 
###############################   GRAVITY MODEL  ###############################
"""

#Import Module
from .geography import Position
from .constant import EarthModel, _DEFAULT_MODEL
import numpy as np

class Gravity():
    def __init__(self,x_ECEF:float,y_ECEF:float,z_ECEF:float,earthModel:str=_DEFAULT_MODEL):
        """create a gravity object based on ECEF coordinates

        Args:
            x_ECEF (float): x coordinate
            y_ECEF (float): y coordinate
            z_ECEF (float): z coordinate
            earthModel (str, optional): name of the Ellipsoid model. Defaults to "WGS84".
        """
        
        self.__positionECEF = Position(x_ECEF,y_ECEF,z_ECEF)
        self.__model = earthModel
 
    @classmethod
    def fromPosition(cls,pos:Position,earthModel:str=_DEFAULT_MODEL):
        """Create a gravity object based on dragonFly.geography.Position Object

        Args:
            pos (Position)              : Position object
            earthModel (str, optional)  : name of the Earth model. Defaults to _DEFAULT_MODEL.

        Returns:
            gravity: gravity instance
        """
        return Gravity(pos.x,pos.y, pos.z,earthModel)
    
    @classmethod
    def fromLLA(cls,latitude:float,longitude:float,altitude:float,earthModel:str=_DEFAULT_MODEL):
        """Create a gravity object based on Latitude Longitude and altitude information

        Args:
            latitude (float): latitude in radians
            longitude (float): longitude in radians
            altitude (float): altitude in meters 
            earthModel (str, optional): name of the Earth model. Defaults to _DEFAULT_MODEL.

        Returns:
            gravity: gravity instance
        """
        return Gravity.fromPosition(Position.fromLLA(latitude,longitude,altitude),earthModel)

    def toList(self):
        """Provide gravity vector as a Python list in ECEF frame

        Returns:
            list : list [3 elements] of the ECEF coordinates of the gravity vector
        """
        return self.__calculateGravity()

    def toNumpy(self):
        """Provide gravity vector as a numpy vector in ECEF frame

        Returns:
            np.ndarray : column vector [3x1] of the ECEF coordinates of the gravity vector
        """
        return np.reshape(np.array(self.__calculateGravity()),(3,-1))
    
    def __calculateGravity(self):
        """PRIVATE FUNCTION -  calculate the gravity vector based on ECEF coordinates and ellipsoid model
        """

        #get gravitation parameter
        earth = EarthModel(self.__model)

        position=self.__positionECEF
        
        # get constant
        a  = earth.a
        mu = earth.mu
        J2 = earth.j2

        # get norm of ECEF coordinate
        r = position.norm

        gx =-mu/r**2*(1+3/2*J2*(a/r)**2*(1-5*(position.z/r)**2))*position.x/r
        gy =-mu/r**2*(1+3/2*J2*(a/r)**2*(1-5*(position.z/r)**2))*position.y/r
        gz =-mu/r**2*(1+3/2*J2*(a/r)**2*(3-5*(position.z/r)**2))*position.z/r

        return [gx,gy,gz]