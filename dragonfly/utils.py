"""
########################  UTILS  ########################

collect all the utility fonction of dragonFly

"""

# import module
import numpy as np
import os
from scipy.spatial.transform import Rotation
from typing import Any, List, Tuple


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

# ===============================  Error Message  ========================


def __createErrorMessageData(errorMsg, value):
    msg = (f"{errorMsg}\n" +
           f"Current Value    : {value}\n" +
           f"Curent Data Type : {type(value)}"
           )
    return msg


def __createErrorMessage(errorMsg: str,
                         expectedValue: str,
                         realValue: str) -> str:
    """PRIVATE - create a generic error message

    Args:
        errorMsg (str): description of the error
        expectedValue (str): expected information
        realValue (str): assessed information

    Returns:
        str: _description_
    """
    msg = (
        f"{errorMsg}\n" +
        f"Expected : {expectedValue}\n" +
        f"Real:      {realValue}\n"
    )
    return msg

# ===============================  FILE FOLDER =========================


def __validateFile(filepath: str) -> str:
    """check if the file exists and provide the absolute path

    Args:
        filepath (str): file path to asses (relative or absolute)

    Returns:
        str: absolute path
    """

    # chech arguments:
    filepath = __validateInstance(filepath, str)

    # Analysis
    try:
        if os.path.isfile(filepath):
            return os.path.abspath(filepath)
    except Exception as e:
        msg = f"impossible to assess the arg1 [{filepath}]"
        raise Exception(msg).with_traceback(e.__traceback__)

    msg = f"The path {filepath} is not an existing file "
    msg = __createErrorMessage(
        msg,
        "Existing file",
        f"Not a file [{filepath}]"
    )
    raise ValueError(msg)


def __validateFileExtension(filepath: str, validExtension: list[str]) -> str:
    return "False"


def __validateFolder(folderpath: str) -> str:
    """check if the file exists and provide the absolute path

    Args:
        folderpath (str): folder path to asses (relative or absolute)

    Returns:
        str: absolute path of the existing folder
    """

    # chech arguments:
    folderpath = __validateInstance(folderpath, str)

    # Analysis
    try:
        if os.path.isdir(folderpath):
            return os.path.abspath(folderpath)
    except Exception as e:
        msg = f"impossible to assess the arg1 [{folderpath}]"
        raise Exception(msg).with_traceback(e.__traceback__)

    msg = f"The path {folderpath} is not an existing folder "
    msg = __createErrorMessage(
        msg,
        "Existing folder",
        f"Not a folder [{folderpath}]"
    )
    raise ValueError(msg)

# ===================== DATA VALIDATION ===========================


def __validateInstance(
    data: Any,
    instances: type | List[type] | Tuple[type],
    inheritance: bool = False
) -> Any:
    """validate if a data as the appropriate type

    Args:
        data (Any): data to assess
        instances (type | Tuple[type]): expected types
        inheritance (bool, optional): inheritance activated
            Defaults to False.

    Returns:
        Any: same object as data
    """

    # Nested evaluation function
    def evaluateType(data, listTypes, inheritance) -> bool:
        if inheritance:
            # with inheritance
            return isinstance(data, listTypes)
        else:
            # inheritance is disable
            return type(data) in listTypes

    # check the list of accepted types
    if isinstance(instances, type):
        listTypes = (instances,)  # force to have a one element tuple
    elif (isinstance(instances, tuple) and
          all(isinstance(elem, type) for elem in instances)):
        listTypes = instances
    else:
        msg = "__validateInstance() arg 2 must be a type or a tuple of types"
        msg = __createErrorMessage(
            msg,
            "type or tuple of types",
            type(data)
        )
        raise ValueError(msg)

    if evaluateType(data, listTypes, inheritance):
        return data

    # raise error
    msg = ("The input shall respected the"
           f" expected types (inheritance: {inheritance})")
    msg = __createErrorMessage(msg, instances, type(data))
    raise TypeError(msg)


def __validateListInstances(dataList: List, instances) -> List:
    raise NotImplementedError("To be done")


def __validateTupleInstances(dataList: Tuple, instances) -> List:
    raise NotImplementedError("To be done")


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
