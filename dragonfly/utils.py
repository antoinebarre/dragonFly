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
    return Rotation.from_rotvec(theta * np.array([1, 0, 0])).as_matrix()

def roty(theta:float)->np.ndarray:
    """provide the rotational matrix of an angle of theta along the y axis

    Args:
        theta (float): angle of rotation defined in radians

    Returns:
        np.ndarray: rotational matrix [3x3]
    """
    return Rotation.from_rotvec(theta * np.array([0, 1, 0])).as_matrix()

def rotz(theta:float)->np.ndarray:
    """provide the rotational matrix of an angle of theta along the z axis

    Args:
        theta (float): angle of rotation defined in radians

    Returns:
        np.ndarray: rotational matrix [3x3]
    """
    return Rotation.from_rotvec(theta * np.array([0, 0, 1])).as_matrix()