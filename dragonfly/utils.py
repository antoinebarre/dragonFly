"""
########################  UTILS  ######################## 

collect all the utility fonction of dragonFly

"""

#import module
import numpy as np
from scipy.spatial.transform import Rotation


def assertInstance(data_name:str,data:str,expected_Instance:str)->None:
    """PRIVATE TOOLS - used to standardize the error message for Instance assessment in dragonFly

    Args:
        data_name (str): _description_
        data (str): _description_
        expected_Instance (str): _description_
    """

    if not isinstance(data,expected_Instance):
        message = f"{data_name} shall be of the following type(s) : {expected_Instance} [current{type(data)}] "
        raise TypeError(message)

#-----------------------------------------------------------------------------
# ROTATION MATRIX

def rotx(theta:float)->np.ndarray:
    """provide the rotational matrix of an angle of theta along the x axis

    Args:
        theta (float): angle of rotation defined in radians

    Returns:
        np.ndarray: rotational matrix [3x3]
    """
    return __fundamentalRotation(np.array([1, 0, 0]),theta)

def roty(theta:float)->np.ndarray:
    """provide the rotational matrix of an angle of theta along the y axis

    Args:
        theta (float): angle of rotation defined in radians

    Returns:
        np.ndarray: rotational matrix [3x3]
    """
    return __fundamentalRotation(np.array([0, 1, 0]),theta)

def rotz(theta:float)->np.ndarray:
    """provide the rotational matrix of an angle of theta along the z axis

    Args:
        theta (float): angle of rotation defined in radians

    Returns:
        np.ndarray: rotational matrix [3x3]
    """
    return __fundamentalRotation(np.array([0, 0, 1]),theta)

def __fundamentalRotation(axis:np.ndarray,theta)->np.ndarray:
    """PRIVATE FUNCTION - create rotation matrix based on angle and axis"""

    try:
        theta = float(theta)
        return Rotation.from_rotvec(theta * axis).as_matrix().T    
    except TypeError:
        raise TypeError('The angle of rotation shall be a scalar not a list or a tuple')
    except ValueError:
        raise ValueError('The angle shall be a number')

    