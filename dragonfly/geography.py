"""SUBMODULE GEOGRAPHY
    This module contains all the geographic utilities for the DragonFlly application


LIST OF CLASSES:
    - Position : geographic position classes
"""

#MODULES IMPORT
import numpy as np
import math
from  .constant import EarthModel
from  .utils import assertInstance


#######################################################################################################################
#                                                                                                                     #
#                                                   CLASS POSITION                                                    #
#                                                                                                                     #
#######################################################################################################################


class Position:
    """Class for the management of ECEF position
    """

    def __init__(self,x:float,y:float,z:float):
        """create a Position object based on ECEF coordinates

        Args:
            x (float): x coordinates in ECEF
            y (float): y coordinates in ECEF
            z (float): z coordinates in ECEF
        """
        self.x = x
        self.y = y
        self.z = z

    def __getattr__(self, name: str):
        return self.__dict__[f"_{name}"]

    def __setattr__(self, name, value):
        # see https://realpython.com/python-getter-setter/ for more details

        try:
            self.__dict__[f"_{name}"] = float(value)

        except TypeError:
             raise TypeError(f'"{name}" shall be a scalar not a list or a tuple')
        except ValueError:
             raise ValueError(f'"{name}" shall be a number') from None

################################## IMPORTER ##################################
    @classmethod
    def fromList(cls,data:list):
        """Create a instance of position (or a list) based on a list of cartesian position in ECEF reference

        Args:
            data (list): position X,Y,Z in meter (or a nested list of [X,Y,Z])

        Returns:
            object : position object or a list of position object
        """

        #check if nested list:
        if any(isinstance(ix, list) for ix in data):
            return Position.__fromNestedList(data)
        else:
            return Position.__from1DList(data)
  
    @classmethod
    def __from1DList(cls,data:list):
        """PRIVATE METHOD : create Position from a 1D list"""
        #IO VERIFICATION
        if not isinstance(data,list):
            raise TypeError(f"data shall be a list  [current: {type(data)}] ")
        if len(data)!=3:
            raise ValueError(f"data shall be a list of 3 elements [current: {len(data)}] ")
        
        return Position(data[0],data[1],data[2])

    @classmethod
    def __fromNestedList(cls,datas:list):
        """PRIVATE METHOD : create Position from a Nested list"""

        newObj = [Position.__from1DList(data) for data in datas]
        return newObj
    
    @classmethod
    def fromLLA(cls, lat:float,long:float,alt:float,ellipsoid:str = "WGS84"):
        """create a position object based on geodetic position (ie. latitude, longitude, altitude)

        Args:
            lat (float): latitude in radians
            long (float): longitude in radians
            alt (float): altitude in meters
            ellipsoid (str, optional): Model of Earth Ellipsoid. Defaults to "WGS84".

        Returns:
            obj: instance of Position Class
        """

        #IO management
        assertInstance("latitude",lat,(float,int,long))
        assertInstance("longitude",long,(float,int,long))
        assertInstance("altitude",alt,(float,int,long))


        #create EarthModel
        earth = EarthModel(ellipsoid)

        #constante
        a       = earth.a
        e2      = earth.e**2

        # transofrmation algorithm
        sinlat = math.sin(lat)
        coslat = math.cos(lat)

        N = a / math.sqrt(1 - e2 * sinlat**2)

        #Calculate ECEF position
        X = (N + alt) * coslat * np.cos(long)
        Y = (N + alt) * coslat * np.sin(long)
        Z = (N*(1 - e2) + alt) * sinlat


        return Position(X,Y,Z)


################################## EXPORTER ##################################

    def toLLA(self,ellipsoid:str = "WGS84"):
        """return the geographic position (i.e. latitude, longitude and altitude) against an Ellipsoid model (by default WGS84)

        Args:
            ellipsoid (str, optional): Ellispoid reference. Defaults to "WGS84".

        Returns:
            float : latitude in radians
            float : longitude in radians
            float : altitude in radians
        """
        
        #create EarthModel
        earth = EarthModel(ellipsoid)

        #constante
        a       = earth.a
        b       = earth.b
        f       = earth.f
        e       = earth.e
        e2      = e**2       # Square of first eccentricity
        ep2     = e2 / (1 - e2)    # Square of second eccentricity

        # Longitude
        longitude   = math.atan2(self.y,self.x)

        # Distance from Z-axis
        D           = math.hypot(self.x,self.y)

        # Bowring's formula for initial parametric (beta) and geodetic (phi) latitudes
        beta        = math.atan2(self.z, (1 - f) * D)
        phi         = math.atan2(self.z   + b * ep2 * math.sin(beta)**3, D - a * e2  * math.cos(beta)**3)

        #Fixed-point iteration with Bowring's formula
        # (typically converges within two or three iterations)
        betaNew     = math.atan2((1 - f)*math.sin(phi), math.cos(phi))
        count       = 0

        while beta != betaNew and count < 1000:

            beta = betaNew
            phi = math.atan2(self.z   + b * ep2 * math.sin(beta)**3,D - a * e2  * math.cos(beta)**3)
            betaNew = math.atan2((1 - f)*math.sin(phi), math.cos(phi))
            count += 1
        

        # Calculate ellipsoidal height from the final value for latitude
        sinphi = math.sin(phi)
        N = a / math.sqrt(1 - e2 * sinphi**2)
        altitude = D * math.cos(phi) + (self.z + e2 * N * sinphi) * sinphi - N

        latitude = phi
   

        # voir https://github.com/kvenkman/ecef2lla/blob/master/ecef2lla.py
        return latitude,longitude,altitude