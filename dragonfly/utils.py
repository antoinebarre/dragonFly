"""
########################  UTILS  ########################

collect all the utility fonction of dragonFly

"""

# import module
import numpy as np
import os
from scipy.spatial.transform import Rotation
from typing import Any, List, Tuple
import pathlib


# EXCEPTION CREATOR


class InvalidFileExtension(Exception):
    "Raised when the file path has not the appropriate extension"
    pass


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


# ============================================================================
#                           INPUTS CHECKS NUMPY        
# ============================================================================


def __input_check_3x1(x_in):
    """PRIVATE FUNCTIION - check if the input is
    mutable to a [3x1] numpy array"""

    if (isinstance(x_in, np.ndarray) and
       list(x_in.shape) in [[3], [3, 1], [1, 3]]):
        return np.reshape(x_in, (3, -1))
    elif (isinstance(x_in, (list, tuple)) and
          len(x_in) == 3 and all(isinstance(i, (float, int)) for i in x_in)):
        return np.reshape(np.array(x_in), (3, -1))
    
    # Raise Error
    msg = __createErrorMessage(
        errorMsg= "The input shall be mutable to a [3x1] numpy array",
        expectedValue= "[3x1] Numpy Array",
        realValue= f"Values: {x_in} - Type: {type(x_in)}",
    )
    raise ValueError(msg)


def __input_check_3x3(x_in):
    """PRIVATE FUNCTION - check if the input is a [3x3] numpy array"""
    if isinstance(x_in, np.ndarray) and x_in.shape == (3, 3):
        return x_in
   
    # raise error
    msg = __createErrorMessage(
        errorMsg="The input shall a [3x3] numpy array",
        realValue=f"Values: {x_in} - Type: {type(x_in)}"
    )
    raise ValueError(msg)

# ===============================  Error Message  ========================

def __createErrorMessage(errorMsg: str,
                         expectedValue: str ="",
                         realValue: str ="") -> str :
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
        f"Current :  {realValue}\n"
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


def __validateFileExtension(
    filepath: str,
    validExtensions: str | tuple[str]
) -> str:
    """Validate the File extension against a list of valid file extension

    Args:
        filepath (str): file path (relative or absolute)
        validExtensions (str | tuple[str]): list of valid extensions
                                            (shall start with ".")

    Returns:
        str: copy of the file path if the extension is correct
    """

    # arguments validation
    filepath = __validateInstance(filepath, str)
    tupleExtension = __validateExtensionDefinition(validExtensions)

    # get the extension
    file_extension = pathlib.Path(filepath).suffix
    
    if file_extension in tupleExtension:
        return filepath

    # raise error

    msg = f"The file [{filepath}] has not the appropriate extension"
    msg = __createErrorMessage(msg, tupleExtension, file_extension)
    raise InvalidFileExtension(msg)


def isValidExtension(
    filepath: str,
    expectedExtensions: str | tuple[str]
) -> bool:
    """check if a path has an appropriate extension

    Args:
        filepath (str): file path to test
        expectedExtensions (str | tuple[str]): list of valid extension
                                               (shall start with ".")

    Returns:
        bool: True if Valid or False else
    """

    # call the __validateFileExtension function
    try:
        filepath = __validateFileExtension(filepath, expectedExtensions)
        return True
    except InvalidFileExtension:
        return False
    except Exception as Exc:
        raise Exc


def __validateExtensionDefinition(
        extension2validate: str | tuple[str]) -> tuple[str]:
    """Validate if a string is an appropriate extensions definition
    (ie. start with a point) and return the same data if OK as a tuple

    Args:
        extension2validate (str | tuple[str]): extension definition to validate

    Returns:
        tuple[str]: tuple of valid extension
    """
    # check if string
    extension2validate=__validateTupleInstances(extension2validate, str)
    
    if all(elem.startswith('.') for elem in extension2validate):
        return extension2validate
    
    # raise error
    msg = __createErrorMessage(
        errorMsg=(
            "The extension definition shall start with '.'"
        ),
        expectedValue="example '.py', '.txt'",
        realValue=f"{extension2validate}"
    )
    raise ValueError(msg)


def __validateFolder(folderpath: str) -> str:
    """check if the folder exists and provide the absolute path

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


def listdirectory(dirpath: str, *,
                  extensions: str | tuple[str] = (),
                  excluded_folders: str | tuple[str] = ()) -> list[str]:
    """get the list of the files in a directory and subdirectories
    with possibility to select extensions and exclude some folders

    Args:
        dirpath (str): path of the directory to assess (absolute or relative)
        extensions (str | tuple[str], optional): tuple of the
         selected extension.
            Defaults all with ().
        excluded_folders (str | tuple[str], optional): tuple of
         folders to exclude.
            Defaults all with ().

    Returns:
        list[str]: _description_
    """
    # define folder exclusion strategy
    grab_all_folders = False
    if not excluded_folders:
        grab_all_folders = True

    # define extension strategy
    if not extensions:
        grab_all_extensions = True
    else:
        extensions = __validateExtensionDefinition(extensions)
        grab_all_extensions = False

    # initiate result
    result = set()

    # iterate over files
    for dir_, _, files in os.walk(dirpath):

        if ((not any(substring in dir_
                     for substring in excluded_folders))
           or grab_all_folders):
            for file_name in files:
                if ((pathlib.Path(file_name).suffix in extensions)
                   or grab_all_extensions):
                    rel_dir = os.path.relpath(dir_, dirpath)
                    rel_file = os.path.join(rel_dir, file_name)
                    result.add(rel_file)

    return list(result)


def __readASCIIFile(filePath: str | bytes | os.PathLike) -> str:
    """PRIVATE - read an existing ASCII File

    Args:
        filePath (str | bytes | os.PathLike): file path (absolute or relative)

    Returns:
        str: contents of the file
    """
    return pathlib.Path(filePath).read_text()


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
    listTypes = __validateTupleInstances(
        data=instances,
        instance=type,
    )

    if evaluateType(data, listTypes, inheritance):
        return data

    # raise error
    msg = __createErrorMessage(
        errorMsg=("The input shall respected the"
                  f" expected types (inheritance: {inheritance})"),
        expectedValue=instances,
        realValue=f"{data} ({type(data)})",
    )
    raise TypeError(msg)


def __validateListInstances(data: Any, instance) -> List:
    """Check if data is a list of instance object

    Args:
        data (any): object to analyze (instance object or list of instance objects)
        instance (type): type of the content of the expected list

    Returns:
        list: list of instance objects
    """
    
    # check instance data type
    if (not isinstance(instance,type)) or instance in (list,set,tuple):
        msg = __createErrorMessage(
            errorMsg=((
                "the instance object shall be"
                " a Type object different of list, tuple or set"
            )),
            expectedValue=type,
            realValue=f"{instance} ({type(instance)})",
        )
        raise TypeError(msg)

    if isinstance(data, instance):
        return [data,]  # force to have a one element tuple
    elif (isinstance(data, list) and
          all(isinstance(elem, instance) for elem in data)):
        return data

    # Raise error
    msg = __createErrorMessage(
        errorMsg= (f"The data shall be a {str(instance)}"
                   f" or a list of {str(instance)}"),
        expectedValue=(f"{str(instance)} object "
                       f"or list of {str(instance)} objects"),
        realValue=data
    )
    raise TypeError(msg)


def __validateTupleInstances(data: any, instance:type) -> tuple:
    """Check if data is a tuple of instance object

    Args:
        data (any): object to analyze (instance object or tuple of instance objects)
        instances (type): type of the content of the expected tuple

    Returns:
        tuple: tuple of instance objects
    """
    
    # check instance data type
    if (not isinstance(instance,type)) or instance in (list,set,tuple):
        msg = __createErrorMessage(
            errorMsg=((
                "the instance object shall be"
                " a Type object different of list, tuple or set"
            )),
            expectedValue=type,
            realValue=f"{instance} ({type(instance)})",
        )
        raise TypeError(msg)

    if isinstance(data, instance):
        return (data,)  # force to have a one element tuple
    elif (isinstance(data, tuple) and
          all(isinstance(elem, instance) for elem in data)):
        return data

    # Raise error
    msg = __createErrorMessage(
        errorMsg= (f"The data shall be a {str(instance)}"
                   f" or a tuple of {str(instance)}"),
        expectedValue=(f"{str(instance)} object "
                       f"or Tuple of {str(instance)} objects"),
        realValue=data
    )
    raise TypeError(msg)


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
