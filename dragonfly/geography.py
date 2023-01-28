"""SUBMODULE GEOGRAPHY
    This module contains all the geographic utilities for
    the DragonFlly application
"""

# MODULES IMPORT
import numpy as np
import math
from .constant import EarthModel, _DEFAULT_MODEL
from .utils import _assertInstance
from .utils import rotx, roty, rotz

"""
----------- POSITION CLASS -----------

"""


class Position:
    """Class for the management of ECEF position
    """

    def __init__(self, x: float, y: float, z: float):
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
            raise TypeError(
                f'"{name}" shall be a scalar not a list or a tuple')
        except ValueError:
            raise ValueError(
                f'"{name}" shall be a number') from None

    def __repr__(self):
        """internal method for the print"""
        return f"ECEF Coordinates:\nx : {self.x}\ny : {self.y}\nz : {self.z}"

    def __eq__(self, __o: object) -> bool:
        """internal method for equality"""
        if isinstance(__o, Position):
            return (self.x, self.y, self.z) == (__o.x, __o.y, __o.z)
        raise NotImplementedError(
            "Class Position equality with" +
            f" this data type [{type(__o)} is not implemented]")

    def __sub__(self, __o: object) -> bool:
        """internal method for equality"""
        if isinstance(__o, Position):
            return Position(self.x - __o.x, self.y - __o.y, self.z - __o.z)

        msg = (
            f"Class Position equality with this data type [{type(__o)}"
            " is not implemented]"
        )
        raise NotImplementedError(msg)

# IMPORTER:
    @classmethod
    def fromList(cls, data: list):
        """Create a instance of position (or a list) based on a list of
        cartesian position in ECEF reference

        Args:
            data (list): position X,Y,Z in meter (or a nested list of [X,Y,Z])

        Returns:
            object : position object or a list of position object
        """

        # check if nested list:
        if any(isinstance(ix, list) for ix in data):
            return Position.__fromNestedList(data)
        else:
            return Position.__from1DList(data)

    @classmethod
    def __from1DList(cls, data: list):
        """PRIVATE METHOD : create Position from a 1D list"""
        # IO VERIFICATION
        if not isinstance(data, list):
            raise TypeError(f"data shall be a list  [current: {type(data)}] ")
        if len(data) != 3:
            msg = (
                f"data shall be a list of 3 elements [current: {len(data)}] "
            )
            raise ValueError(msg)

        return Position(data[0], data[1], data[2])

    @classmethod
    def __fromNestedList(cls, datas: list):
        """PRIVATE METHOD : create Position from a Nested list"""

        newObj = [Position.__from1DList(data) for data in datas]
        return newObj

    @classmethod
    def fromLLA(cls, lat: float, long: float, alt: float,
                ellipsoid: str = _DEFAULT_MODEL):
        """create a position object based on geodetic
        position (ie. latitude, longitude, altitude)

        Args:
            lat (float): latitude in radians
            long (float): longitude in radians
            alt (float): altitude in meters
            ellipsoid (str, optional): Model of
                Earth Ellipsoid. Defaults to "WGS84".

        Returns:
            obj: instance of Position Class
        """

        # IO management
        _assertInstance("latitude", lat, (float, int, long))
        _assertInstance("longitude", long, (float, int, long))
        _assertInstance("altitude", alt, (float, int, long))

        # create EarthModel
        earth = EarthModel(ellipsoid)

        # constante
        a = earth.a
        e2 = earth.e**2

        # transofrmation algorithm
        sinlat = math.sin(lat)
        coslat = math.cos(lat)

        N = a / math.sqrt(1 - e2 * sinlat**2)

        # Calculate ECEF position
        X = (N + alt) * coslat * np.cos(long)
        Y = (N + alt) * coslat * np.sin(long)
        Z = (N*(1 - e2) + alt) * sinlat

        return Position(X, Y, Z)

# ------------------------- PROPERTIES -------------------------
    @property
    def norm(self):
        return np.linalg.norm([self.x, self.y, self.z])

# ------------------------- EXPORTER -------------------------

    def toNumpy(self):
        """Provide Postion ECEF vector as a numpy vector

        Returns:
            np.ndarray : column vector [3x1] of the ECEF coordinates
        """
        return np.reshape(np.array([self.x, self.y, self.z]), (3, -1))

    def toLLA(self, ellipsoid: str = _DEFAULT_MODEL):
        """return the geographic position (i.e. latitude, longitude and
        altitude) against an Ellipsoid model (by default WGS84)

        Args:
            ellipsoid (str, optional): Ellispoid reference.
            Defaults to "WGS84".

        Returns:
            float : latitude in radians
            float : longitude in radians
            float : altitude in radians
        """

        # create EarthModel
        earth = EarthModel(ellipsoid)

        # constante
        a = earth.a
        b = earth.b
        f = earth.f
        e = earth.e
        e2 = e**2       # Square of first eccentricity
        ep2 = e2 / (1 - e2)    # Square of second eccentricity

        # Longitude
        longitude = math.atan2(self.y, self.x)

        # Distance from Z-axis
        D = math.hypot(self.x, self.y)

        # Bowring's formula for initial parametric
        # (beta) and geodetic (phi) latitudes
        beta = math.atan2(self.z, (1 - f) * D)
        phi = math.atan2(self.z + b * ep2 * math.sin(beta)**3,
                         D - a * e2 * math.cos(beta)**3)

        # Fixed-point iteration with Bowring's formula
        # (typically converges within two or three iterations)
        betaNew = math.atan2((1 - f)*math.sin(phi), math.cos(phi))
        count = 0

        while beta != betaNew and count < 1000:

            beta = betaNew
            phi = math.atan2(self.z + b * ep2 * math.sin(beta)**3,
                             D - a * e2 * math.cos(beta)**3)
            betaNew = math.atan2((1 - f)*math.sin(phi),
                                 math.cos(phi))
            count += 1

        # Calculate ellipsoidal height from the final value for latitude
        sinphi = math.sin(phi)
        N = a / math.sqrt(1 - e2 * sinphi**2)
        altitude = D * math.cos(phi) + (self.z + e2 * N * sinphi) * sinphi - N

        latitude = phi

        # voir https://github.com/kvenkman/ecef2lla/blob/master/ecef2lla.py
        return latitude, longitude, altitude


"""
-------------------- ROTATION MATRIX --------------------
"""


def DCM_ECI2ECEF(dt: float) -> np.ndarray:
    """Provide the Direct Cosine Matrix to convert Earth-centered inertial
     (ECI) to Earth-centered Earth-fixed (ECEF) coordinates

    - The x-axis points towards the vernal equinox (First Point of Aries ♈).
    - The y-axis points 90 degrees to the east of the x-axis in the equatorial
        plane.
    - The z-axis points northward along the Earth rotation axis.

    Args:
        dt (float): time in second since the user defined the Earth Center
        Inertial (ECI) frame. This value shall be positive (>=0)

    Returns:
        np.ndarray: rotational matrix [3x3] to transform a vector in ECI in
        the ECEF frame
    """

    # voir https://github.com/NavPy/NavPy/blob/master/navpy/core/navpy.py

    return rotz(EarthModel.earthRotationRate * dt)


def dcm_ecef2ned(latitude: float, longitude: float) -> np.ndarray:
    """Calculate the rotational matrix from the ECEF (Earth Centered Earth
    Fixed) to NED (North Earth Down) to transform a vector defined in ECEF
    to NED frame

    Args:
        latitude (float): latitude of the geographical point in radians
        longitude (float): longitude of the geographical point in radians

    Returns:
        np.ndarray: Direct Cosinus Matrix from ECEF to NED
    """

    M = np.matmul(roty(-(latitude + np.pi / 2)), rotz(longitude))

    return M


def dcm_ecef2enu(latitude: float, longitude: float) -> np.ndarray:
    """Calculate the rotational matrix from the ECEF (Earth Centered Earth
     Fixed) to ENU (East North Up) to transform a vector defined in ECEF to
     ENU frame

    Args:
        latitude (float): latitude of the geographical point in radians
        longitude (float): longitude of the geographical point in radians

    Reference:
        https://gssc.esa.int/navipedia/index.php/Transformations_between_ECEF_and_ENU_coordinates

    Returns:
        np.ndarray: Direct Cosinus Matrix from ECEF to ENU
    """

    return (
        rotx(np.pi / 2) @ rotz(np.pi / 2) @ roty(-latitude) @ rotz(longitude)
    )  # np.matmul(roty(-latitude+np.pi/2),rotz(np.pi/2+longitude))


def angle2dcm(rotAngle1: float, rotAngle2: float,
              rotAngle3: float, rotationSequence: str = 'ZYX') -> np.ndarray:
    """This function converts Euler Angle into Direction Cosine Matrix (DCM).
    Args:
        rotAngle1 (float): first angle of roation in radians
            (e.g. yaw for 'ZYX')
        rotAngle2 (float): second angle of roation in radians
            (e.g. pitch for 'ZYX')
        rotAngle3 (float): third angle of roation in radians
            (e.g. roll for 'ZYX')
        rotationSequence (str, optional): sequence of rotations.
            Defaults to 'ZYX'.

    Returns:
        np.ndarray: direction cosine matrix associated to the rotation angles
    """

    if rotationSequence.upper() == "ZYX":
        return rotx(rotAngle3)@roty(rotAngle2)@rotz(rotAngle1)
    else:
        msg = (f"Rotation sequence {rotationSequence.upper()}"
               " is not implemented.")
        raise NotImplementedError(msg)


def dcm2angle(dcm: np.ndarray,
              rotationSequence: str = 'ZYX') -> tuple[float, float, float]:
    """This function converts a Direction Cosine Matrix (DCM) into the three
    rotation angles.

    Notes:
    The returned rotAngle1 and 3 will be between   +/- 180 deg (+/- pi rad).
    In contrast, rotAngle2 will be in the interval +/- 90 deg (+/- pi/2 rad).
    In the 'ZYX' or '321' aerospace sequence, that means the pitch angle
    returned will always be inside the closed interval +/- 90 deg
    (+/- pi/2 rad).
    Applications where pitch angles near or larger than 90 degrees
    in magnitude are expected should used alternate attitude parameterizations
    like quaternions.

    Args:
        dcm (np.ndarray): direction cosine matrix associated
            to the rotation angles
        rotationSequence (str, optional): sequence of rotations.
            Defaults to 'ZYX'.

    Returns:
        rotAngle1 (float): first angle of roation in radians
            (e.g. yaw for 'ZYX')
        rotAngle2 (float): second angle of roation in radians
            (e.g. pitch for 'ZYX')
        rotAngle3 (float): third angle of roation in radians
            (e.g. roll for 'ZYX')
    """

    if rotationSequence.upper() == "ZYX":
        rotAngle1 = np.arctan2(dcm[0, 1], dcm[0, 0])   # Yaw
        rotAngle2 = -np.arcsin(dcm[0, 2])  # Pitch
        rotAngle3 = np.arctan2(dcm[1, 2], dcm[2, 2])  # Roll

        return rotAngle1, rotAngle2, rotAngle3
    else:
        msg = (f"Rotation sequence {rotationSequence.upper()}"
               " is not implemented.")
        raise NotImplementedError(msg)


def getRange(lat1: float, long1: float, lat2: float, long2: float,
             earth_model: str = _DEFAULT_MODEL,
             nbIter: int = 200) -> float:
    """Calculate the distance between two points on the surface of a spheroid

    Args:
        lat1 (float): initial latitude in radians
        long1 (float): initial longitude in radians
        lat2 (float): final latitude in radians
        long2 (float): final initial longitude in radians
        earth_model (str, optional): _description_. Defaults to "WGS84".

    Returns:
        float: distance in meters
    """

    # latitue assertion
    msg = ("Latitudes Value shall be lower than 90"
           f" (lat1: {np.rad2deg(lat1)} , lat2: {np.rad2deg(lat2)})")

    assert abs(lat1) <= np.pi/2 and abs(lat2) <= np.pi/2, msg

    # short-circuit coincident points
    if lat1 == lat2 and long1 == long2:
        return 0.0

    # load earth model
    earth = EarthModel(earth_model)
    a = earth.a
    b = earth.b
    f = earth.f

    # constant
    CONVERGENCE_THRESHOLD = 1e-12

    # correct for errors at exact poles by adjusting 0.6 millimeters:
    if np.absolute(np.pi/2-np.absolute(lat1)) < 1e-10:
        lat1 = math.copysign(np.pi/2-(1e-10), lat1)

    if np.absolute(np.pi/2-np.absolute(lat2)) < 1e-10:
        lat2 = math.copysign(np.pi/2-(1e-10), lat2)

    U1 = np.arctan((1 - f) * np.tan(lat1))
    U2 = np.arctan((1 - f) * np.tan(lat2))
    L = long2 - long1
    Lambda = L

    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    for iteration in range(nbIter):
        sinLambda = math.sin(Lambda)
        cosLambda = math.cos(Lambda)
        sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 +
                             (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        if sinSigma == 0:
            return 0.0  # coincident points
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cosSqAlpha = 1 - sinAlpha ** 2
        try:
            cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        except ZeroDivisionError:
            cos2SigmaM = 0
        C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        LambdaPrev = Lambda
        Lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma *
                                               (cos2SigmaM + C * cosSigma *
                                                (-1 + 2 * cos2SigmaM ** 2)))
        if abs(Lambda - LambdaPrev) < CONVERGENCE_THRESHOLD:
            break  # successful convergence
    else:
        return None  # failure to converge

    uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = (B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma *
                  (-1 + 2 * cos2SigmaM ** 2) - B / 6 * cos2SigmaM *
                  (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2))))
    s = b * A * (sigma - deltaSigma)

    return round(s, 4)
