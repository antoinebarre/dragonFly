"""
#======================================================== #
#==================== ROTATION MATRIX =================== #
#======================================================== #
"""

# EXPORT
__all__ = [
    "rotx",
    "roty",
    "rotz",
    "RotationMatrixError",
    "skew_matrix",
]

# IMPORT
import numpy as np
import dragonfly
from scipy.spatial.transform import Rotation

# Rotation Matrix exception


class RotationMatrixError(Exception):
    """Exception raised when the calculation of rotation matrix is impossible
    """
    def __init__(self, axis: np.ndarray, angle: float) -> None:
        self.axis = axis
        self.angle = angle

        msg = ("Impossible to calculate the rotation"
               " matrix with the following parameters:\n"
               f"- Vector: {axis} [type: {type(axis)}]\n"
               f"- Angle: {angle} [type: {type(axis)}]\n")
        self.message = msg

        super().__init__(self.message)


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
        axis = dragonfly.utils.validation.input_check_3x1(axis)
        return Rotation.from_rotvec(theta * axis.reshape((3,))).as_matrix().T
    except BaseException as exc:
        raise RotationMatrixError(axis, theta) from exc


def skew_matrix(vect: np.ndarray) -> np.ndarray:
    """provide the skew symetrical matric of a vector

    Args:
        vect (np.ndarray): column vector [3x1]

    Returns:
        np.ndarray: skew symetrical matric of a vector
    """

    # get input
    vect = dragonfly.utils.validation.input_check_3x1(vect)

    # create matrix
    M = np.array([[0, -vect[2, 0], vect[1, 0]],
                  [vect[2, 0], 0, -vect[0, 0]],
                  [-vect[1, 0], vect[0, 0], 0]])
    return M
