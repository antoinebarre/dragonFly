"""
########################  UTILS  ########################

collect all the utility fonction of dragonFly

"""

# import module
import numpy as np
from scipy.spatial.transform import Rotation


def _assertInstance(data_name: str, data, expected_Instance) -> None:
    """PRIVATE TOOLS - used to standardize the error message for Instance
    assessment in dragonFly

    Args:
        data_name (str): name of the data
        data (str): value to assess
        expected_Instance (str): expected data type
    """

    if not isinstance(data, expected_Instance):
        message = (f"{data_name} shall be of the following type(s) :"
                   f" {expected_Instance} [current{type(data)}] ")
        raise TypeError(message)


"""
-------------------- ROTATION MATRIX --------------------
"""


def rotx(theta: float) -> np.ndarray:
    """provide the rotational matrix of an angle of theta along the x axis

    Args:
        theta (float): angle of rotation defined in radians

    Returns:
        np.ndarray: rotational matrix [3x3]
    """
    return __fundamentalRotation(np.array([1, 0, 0]), theta)


def roty(theta: float) -> np.ndarray:
    """provide the rotational matrix of an angle of theta along the y axis

    Args:
        theta (float): angle of rotation defined in radians

    Returns:
        np.ndarray: rotational matrix [3x3]
    """
    return __fundamentalRotation(np.array([0, 1, 0]), theta)


def rotz(theta: float) -> np.ndarray:
    """provide the rotational matrix of an angle of theta along the z axis

    Args:
        theta (float): angle of rotation defined in radians

    Returns:
        np.ndarray: rotational matrix [3x3]
    """
    return __fundamentalRotation(np.array([0, 0, 1]), theta)


def __fundamentalRotation(axis: np.ndarray, theta) -> np.ndarray:
    """PRIVATE FUNCTION - create rotation matrix based on angle and axis"""
    try:
        theta = float(theta)
        return Rotation.from_rotvec(theta * axis).as_matrix().T
    except TypeError:
        msg = 'The angle of rotation shall be a scalar not a list or a tuple'
        raise TypeError(msg)
    except ValueError:
        raise ValueError('The angle shall be a number')


def skew_matrix(vect: np.ndarray) -> np.ndarray:
    """provide the skew symetrical matric of a vector

    Args:
        vect (np.ndarray): column vector [3x1]

    Returns:
        np.ndarray: skew symetrical matric of a vector
    """

    # get input
    vect = __input_check_3x1(vect)

    # create matrix
    M = np.array([[0, -vect[2, 0], vect[1, 0]],
                  [vect[2, 0], 0, -vect[0, 0]],
                  [-vect[1, 0], vect[0, 0], 0]])
    return M


"""
---------------- INPUTS CHECKS ----------------
"""


def __input_check_3x1(x_in):
    """PRIVATE FUNCTIION - check if the input is
    mutable to a [3x1] numpy array"""

    if (isinstance(x_in, np.ndarray) and
       list(x_in.shape) in [[3], [3, 1], [1, 3]]):
        return np.reshape(x_in, (3, -1))
    elif (isinstance(x_in, (list, tuple)) and
          len(x_in) == 3 and all(isinstance(i, (float, int)) for i in x_in)):
        return np.reshape(np.array(x_in), (3, -1))
    else:
        msg = "The input shall be mutable to a [3x1] numpy array"
        msg = __createErrorMessageData(msg, x_in)
        raise ValueError(msg)


def __input_check_3x3(x_in):
    """PRIVATE FUNCTION - check if the input is a [3x3] numpy array"""
    if isinstance(x_in, np.ndarray) and x_in.shape == (3, 3):
        return x_in
    else:
        msg = "The input shall a [3x3] numpy array"
        msg = __createErrorMessageData(msg, x_in)
        raise ValueError(msg)

# ===============================  TOOLS  ====================================


def __createErrorMessageData(errorMsg, value):
    msg = f"{errorMsg}\n" + \
        f"Current Value    : {value}\n" +\
        f"Curent Data Type : {type(value)}"
    return msg


# ===============================  PROTECTED CLASS  =========================
class ImmutableClass:
    '''Freeze any class such that instantiated
    objects become immutable. Also use __slots__ for speed.

    see: https://medium.datadriveninvestor.com/immutability-in-python-d57a3b23f336 # noqa: E501

    '''
    __slots__ = []
    _frozen = False

    def __init__(self):
        # generate __slots__ list dynamically
        for attr_name in dir(self):
            self.__slots__.append(attr_name)
        self._frozen = True

    def __delattr__(self, *args, **kwargs):
        if self._frozen:
            raise AttributeError('This object is immutable')
        object.__delattr__(self, *args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        if self._frozen:
            raise AttributeError('This object is immutable')
        object.__setattr__(self, *args, **kwargs)
