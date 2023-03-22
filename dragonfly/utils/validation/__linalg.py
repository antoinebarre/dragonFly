"""
#######################################################################
################### LINEAR ALGEBRA VALIDATION TOOLS ###################
#######################################################################
"""

# EXPORTER
__all__ = [
    "input_check_3x1",
    "input_check_3x3",
]

# IMPORT
import numpy as np
import dragonfly
from typing import Any


def input_check_3x1(x_in: Any) -> np.ndarray:
    """Check if a data is mutable to a [3x1] vector numpy array and return it

    Args:
        x_in (Any): data to assess

    Raises:
        ValueError: exception raised if the data is not the appropriate type

    Returns:
        np.ndarray: input as a [3x1] numpy array
    """
    if (isinstance(x_in, np.ndarray) and
       list(x_in.shape) in [[3], [3, 1], [1, 3]]):
        return np.reshape(x_in, (3, -1))
    elif (isinstance(x_in, (list, tuple)) and
          len(x_in) == 3 and all(isinstance(i, (float, int)) for i in x_in)):
        return np.reshape(np.array(x_in), (3, -1))

    # Raise Error
    msg = dragonfly.utils.exception.createErrorMessage(
        errorMsg="The input shall be mutable to a [3x1] numpy array",
        expected="[3x1] Numpy Array",
        current=f"Values: {x_in} - Type: {type(x_in)}",
    )
    raise ValueError(msg)


def input_check_3x3(x_in: Any) -> np.ndarray:
    """check if the input is a [3x3] numpy array

    Args:
        x_in (_type_): data to assess

    Raises:
        ValueError: exception raised if the data is not the appropriate type

    Returns:
        np.ndarray: data as a [3x3] Numpy Array
    """

    if isinstance(x_in, np.ndarray) and x_in.shape == (3, 3):
        return x_in

    # raise error
    msg = dragonfly.utils.exception.createErrorMessage(
        errorMsg="The input shall be a [3x3] numpy array",
        expected="[3x3] numpy array",
        current=f"Values: {x_in} - Type: {type(x_in)}"
    )
    raise ValueError(msg)
