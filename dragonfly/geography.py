"""SUBMODULE GEOGRAPHY
    This module contains all the geographic utilities for the DragonFlly application


LIST OF CLASSES:
    - Position : geographic position classes
"""

#MODULES IMPORT
import datetime
import numpy as np
import math
from  .constant import EarthModel,_DEFAULT_MODEL
from  .utils import _assertInstance
from .utils import rotx, roty, rotz

""" 
888b. .d88b. .d88b. 888 88888 888 .d88b. 8b  8    .d88b 8       db    .d88b. .d88b. 
8  .8 8P  Y8 YPwww.  8    8    8  8P  Y8 8Ybm8    8P    8      dPYb   YPwww. YPwww. 
8wwP' 8b  d8     d8  8    8    8  8b  d8 8  "8    8b    8     dPwwYb      d8     d8 
8     `Y88P' `Y88P' 888   8   888 `Y88P' 8   8    `Y88P 8888 dP    Yb `Y88P' `Y88P'
"""

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

    def __repr__(self):
        """internal method for the print"""
        return f"ECEF Coordinates:\nx : {self.x}\ny : {self.y}\nz : {self.z}"
    
    def __eq__(self, __o: object) -> bool:
        """internal method for equality"""
        if isinstance(__o, Position):
            return (self.x, self.y, self.z) == (__o.x, __o.y,__o.z)
        raise NotImplementedError(f"Class Position equality with this data type [{type(__o)} is not implemented]")


    def __sub__(self, __o: object) -> bool:
        """internal method for equality"""
        if isinstance(__o, Position):
            return Position(self.x-__o.x,self.y-__o.y, self.z-__o.z)
        raise NotImplementedError(f"Class Position equality with this data type [{type(__o)} is not implemented]")

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
    def fromLLA(cls, lat:float,long:float,alt:float,ellipsoid:str = _DEFAULT_MODEL):
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
        _assertInstance("latitude",lat,(float,int,long))
        _assertInstance("longitude",long,(float,int,long))
        _assertInstance("altitude",alt,(float,int,long))


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

################################## PROPERTIES ##################################
    @property
    def norm(self):
        return np.linalg.norm([self.x,self.y, self.z])


################################## EXPORTER ##################################

    def toNumpy(self):
        """Provide Postion ECEF vector as a numpy vector

        Returns:
            np.ndarray : column vector [3x1] of the ECEF coordinates
        """
        return np.reshape(np.array([self.x,self.y,self.z]),(3,-1))

    def toLLA(self,ellipsoid:str = _DEFAULT_MODEL):
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



"""
888b. .d88b. 88888    db    88888 888 .d88b. 8b  8    8b   d8    db    88888 888b. 888 Yb  dP 
8  .8 8P  Y8   8     dPYb     8    8  8P  Y8 8Ybm8    8YbmdP8   dPYb     8   8  .8  8   YbdP  
8wwK' 8b  d8   8    dPwwYb    8    8  8b  d8 8  "8    8  "  8  dPwwYb    8   8wwK'  8   dPYb  
8  Yb `Y88P'   8   dP    Yb   8   888 `Y88P' 8   8    8     8 dP    Yb   8   8  Yb 888 dP  Yb
"""

def DCM_ECI2ECEF(dt:float)->np.ndarray:
    """Provide the Direct Cosine Matrix to convert Earth-centered inertial (ECI) to Earth-centered Earth-fixed (ECEF) coordinates


    The Earth-centered inertial (ECI) system is non-rotating. For most applications, assume this frame to be inertial, although the equinox and equatorial plane move very slightly over time. The ECI system is considered to be truly inertial for high-precision orbit calculations when the equator and equinox are defined at a particular epoch (e.g. J2000). Aerospace functions and blocks that use a particular realization of the ECI coordinate system provide that information in their documentation. The ECI system origin is fixed at the center of the Earth (see figure).

    - The x-axis points towards the vernal equinox (First Point of Aries ♈).
    - The y-axis points 90 degrees to the east of the x-axis in the equatorial plane.
    - The z-axis points northward along the Earth rotation axis.

    
    Args:
        dt (float): time in second since the user defined the Earth Center Intertial (ECI) frame. This value shall be positive (>=0)
        
    Returns:
        np.ndarray: rotational matrix [3x3] to transform a vector in ECI in the ECEF frame
    """

    # voir https://github.com/NavPy/NavPy/blob/master/navpy/core/navpy.py
       
    return rotz(EarthModel.earthRotationRate*dt)

def dcm_ecef2ned(latitude:float,longitude:float)-> np.ndarray:
    """Calculate the rotational matrix from the ECEF (Earth Centered Earth Fixed) to 
    NED (North Earth Down) to transform a vector defined in ECEF to NED frame

    Args:
        latitude (float): latitude of the geographical point in radians
        longitude (float): longitude of the geographical point in radians

    Returns:
        np.ndarray: Direct Cosinus Matrix from ECEF to NED
    """

    M = np.matmul(roty(-(latitude+np.pi/2)),rotz(longitude))
       
    return M


def dcm_ecef2enu(latitude:float,longitude:float)-> np.ndarray:
    """Calculate the rotational matrix from the ECEF (Earth Centered Earth Fixed) to 
    ENU (East North Up) to transform a vector defined in ECEF to ENU frame

    Args:
        latitude (float): latitude of the geographical point in radians
        longitude (float): longitude of the geographical point in radians

    Reference: 
        https://gssc.esa.int/navipedia/index.php/Transformations_between_ECEF_and_ENU_coordinates

    Returns:
        np.ndarray: Direct Cosinus Matrix from ECEF to ENU
    """

    return rotx(np.pi/2)@rotz(np.pi/2)@roty(-latitude)@rotz(longitude)#np.matmul(roty(-latitude+np.pi/2),rotz(np.pi/2+longitude))

def angle2dcm(rotAngle1:float,rotAngle2:float,rotAngle3:float, rotationSequence:str='ZYX')->np.ndarray:
    """This function converts Euler Angle into Direction Cosine Matrix (DCM).
        The DCM is described by three sucessive rotation rotAngle1, rotAngle2, and rotAngle3 about the axes described by the rotation_sequence.
        The default rotation_sequence='ZYX' is the aerospace sequence and rotAngle1 is the yaw angle, rotAngle2 is the pitch angle, and rotAngle3 is the roll angle. In this case DCM transforms a vector from the locally level coordinate frame (i.e. the NED frame) to the body frame.

    Args:
        rotAngle1 (float): first angle of roation in radians (e.g. yaw for 'ZYX')
        rotAngle2 (float): second angle of roation in radians (e.g. pitch for 'ZYX')
        rotAngle3 (float): third angle of roation in radians (e.g. roll for 'ZYX')
        rotationSequence (str, optional): sequence of rotations. Defaults to 'ZYX'.

    Returns:
        np.ndarray: direction cosine matrix associated to the rotation angles
    """

    if rotationSequence.upper()=="ZYX":
        return rotx(rotAngle3)@roty(rotAngle2)@rotz(rotAngle1)
    else:
        msg =f"Rotation sequence {rotationSequence.upper()} is not implemented."
        raise NotImplementedError(msg)

def dcm2angle(dcm:np.ndarray, rotationSequence:str='ZYX')->tuple[float,float,float]:
    """This function converts a Direction Cosine Matrix (DCM) into the three rotation angles.
    The DCM is described by three sucessive rotation rotAngle1, rotAngle2, and rotAngle3 about the axes described by the rotation_sequence.
    The default rotation_sequence='ZYX' is the aerospace sequence and rotAngle1 is the yaw angle, rotAngle2 is the pitch angle, and rotAngle3 is the roll angle. In this case DCM transforms a vector from the locally level coordinate frame (i.e. the NED frame) to the body frame.

    Notes:
    The returned rotAngle1 and 3 will be between   +/- 180 deg (+/- pi rad).
    In contrast, rotAngle2 will be in the interval +/- 90 deg (+/- pi/2 rad). In the 'ZYX' or '321' aerospace sequence, that means the pitch angle returned will always be inside the closed interval +/- 90 deg (+/- pi/2 rad).
    Applications where pitch angles near or larger than 90 degrees in magnitude are expected should used alternate attitude parameterizations like quaternions.

    Args:
        dcm (np.ndarray): direction cosine matrix associated to the rotation angles
        rotationSequence (str, optional): sequence of rotations. Defaults to 'ZYX'.

    Returns:
        rotAngle1 (float): first angle of roation in radians (e.g. yaw for 'ZYX')
        rotAngle2 (float): second angle of roation in radians (e.g. pitch for 'ZYX')
        rotAngle3 (float): third angle of roation in radians (e.g. roll for 'ZYX')
    """


    if rotationSequence.upper()=="ZYX":
        rotAngle1 = np.arctan2(dcm[0, 1], dcm[0, 0])   # Yaw
        rotAngle2 = -np.arcsin(dcm[0, 2])  # Pitch
        rotAngle3 = np.arctan2(dcm[1, 2], dcm[2, 2])  # Roll

        return rotAngle1,rotAngle2,rotAngle3
    else:
        msg =f"Rotation sequence {rotationSequence.upper()} is not implemented."
        raise NotImplementedError(msg)