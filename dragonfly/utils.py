"""
########################  UTILS  ######################## 

collect all the utility fonction of dragonFly

"""

#import module
import numpy as np
from scipy.spatial.transform import Rotation


def _assertInstance(data_name:str,data,expected_Instance)->None:
    """PRIVATE TOOLS - used to standardize the error message for Instance assessment in dragonFly

    Args:
        data_name (str): name of the data
        data (str): value to assess
        expected_Instance (str): expected data type
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

"""
888 8b  8 888b. 8    8 88888 .d88b.    .d88b 8   8 8888 .d88b 8  dP 8888 888b. .d88b. 
 8  8Ybm8 8  .8 8    8   8   YPwww.    8P    8www8 8www 8P    8wdP  8www 8  .8 YPwww. 
 8  8  "8 8wwP' 8b..d8   8       d8    8b    8   8 8    8b    88Yb  8    8wwK'     d8 
888 8   8 8     `Y88P'   8   `Y88P'    `Y88P 8   8 8888 `Y88P 8  Yb 8888 8  Yb `Y88P'
"""

def __input_check_3x1(x_in):
    """PRIVATE FUNCTIION - check if the input is mutable to a [3x1] numpy array"""

    if isinstance(x_in,np.ndarray) and list(x_in.shape) in [[3],[3,1],[1,3]]:
        return np.reshape(x_in,(3,-1))
    elif isinstance(x_in,(list,tuple)) and len(x_in)==3 and all(isinstance(i, (float,int)) for i in x_in):
        return np.reshape(np.array(x_in),(3,-1))
    else:
        msg = __createErrorMessageData("The input shall be mutable to a [3x1] numpy array",x_in)
        raise ValueError(msg)

def __input_check_3x3(x_in):
    """PRIVATE FUNCTION - check if the input is a [3x3] numpy array"""
    if isinstance(x_in,np.ndarray) and x_in.shape == (3,3):
        return x_in
    else: 
        msg = __createErrorMessageData("The input shall a [3x3] numpy array",x_in)
        raise ValueError(msg)

# ===============================  TOOLS  ====================================

def __createErrorMessageData(errorMsg,value):
    msg = f"{errorMsg}\n" + \
        f"Current Value    : {value}\n" +\
        f"Curent Data Type : {type(value)}"
    return msg 