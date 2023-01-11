"""SUBMODULE GEOGRAPHY
    This module contains all the geographic utilities for the DragonFlly application


LIST OF CLASSES:
    - Position : geographic position classes
"""

#MODULES IMPORT
import numpy as np


#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#                                                   CLASS POSITION                                                    #
#                                                                                                                     #
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

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        try:
            self._x = float(value)
        except TypeError:
            raise TypeError('"x" shall be a scalar not a list or a tuple')
        except ValueError:
            raise ValueError('"x" shall be a number') from None

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        try:
            self._y = float(value)
        except TypeError:
            raise TypeError('"y" shall be a scalar not a list or a tuple')
        except ValueError:
            raise ValueError('"y" shall be a number') from None
    
    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        try:
            self._z = float(value)
        except TypeError:
            raise TypeError('"z" shall be a scalar not a list or a tuple')
        except ValueError:
            raise ValueError('"z" shall be a number') from None

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

        if not isinstance(datas,list):
            raise TypeError(f"data shall be a list  [current: {type(datas)}] ")

        newObj = [Position.__from1DList(data) for data in datas]
        return newObj
    
    @classmethod
    def fromLLA(cls, data,ellipsoid:str = "WGS84"):
        pass

################################## EXPORTER ##################################

    def toLLA(self,ellipsoid:str = "WGS84"):
        pass


################################## UTILS ##################################

    @classmethod
    def transform_LLA2ECEF(longitude:np.ndarray,latitude:np.ndarray,altitude:np.ndarray,
                        model:string="WGS84",radians:bool=True):
        """calculate the cartesian coordinates based on the geodetic coordinates (ie. latitude, longitude, altitude)

        Args:
            longitude (np.ndarray): numpy array with latitudes in radians
            latitude (np.ndarray): numpy array with latitudes in radians
            altitude (np.ndarray): numpy array with the altitude in meters
            model (string, optional): Ellipsoid model. Defaults to "WGS84". The available model are WGS72 and WGS84
            radian (bool, optional): if False the latitudes and longitudes are provided in decimal degrees. Defaults to True.

        Returns:
            X,Y,Z : cartesian coordinates in ECEF as np.ndarray
        """
        # TODO : add argument assertion
        
        # Constants:
        LISTMODEL = ["WGS84","WGS72"]
        
        # Argument assertion
        assert model.upper() in (name.upper() for name in LISTMODEL) ,f"Ellipsoid model shall be part of the following list {LISTMODEL}"
        assert isinstance(radians, (bool)) , "radians shall be a boolean"

        # parameter management
        match model.upper():
            case "WGS84":
                ellipsoid = gentraj.constant.WGS84
            case "WGS72":
                ellipsoid = gentraj.constant.WGS72

        if radians == False: #change angle unit to radian
            latitude =np.radians(latitude)
            longitude = np.radians(longitude)

        #Earth parameters
        b = (1-ellipsoid["f"])*ellipsoid["a"]
        e = np.sqrt((ellipsoid["a"]**2-b**2)/ellipsoid["a"]**2)
        e2 = e**2
        

        # transofrmation algorithm
        sinlat = np.sin(latitude)
        coslat = np.cos(latitude)

        N = ellipsoid["a"] / np.sqrt(1 - e2 * sinlat**2)

        X = (N + altitude) * coslat * np.cos(longitude)
        Y = (N + altitude) * coslat * np.sin(longitude)
        Z = (N*(1 - e2) + altitude) * sinlat


        return X,Y,Z