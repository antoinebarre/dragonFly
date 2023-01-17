""" UNIT TESTS FOR INPUT CHECKERS"""

from dragonfly.utils import __input_check_3x1

import pytest
import numpy as np

ABSOLUTE_TOLERANCE = 1e-16
RELATIVE_TOLERANCE = 1e-8


def test_input_check_3x1():
    # wrong data type
    value = "a"
    with pytest.raises(ValueError):
        __input_check_3x1(value)

    value = [1, 2 ,[3 ,4]]
    with pytest.raises(ValueError):
        __input_check_3x1(value)

    # wrong data size with list
    value = [1, 2 ,3 ,4]
    with pytest.raises(ValueError):
        __input_check_3x1(value)

    # wrong data size with Numpy
    value = np.array([1, 2 ,3 ,4])
    with pytest.raises(ValueError):
        __input_check_3x1(value)

    value = np.array([[1, 2 ,3],[4,5,6]])
    with pytest.raises(ValueError):
        __input_check_3x1(value)

    # good data 1D Numpy
    value = np.array([1,2,3])
    expectedValue = np.array([[1],[2],[3]])
    assess_NP_object(__input_check_3x1(value),expectedValue)

    # good data 
    value = np.array([[1],[2],[3]])
    expectedValue = np.array([[1],[2],[3]])
    
    assess_NP_object(__input_check_3x1(value),expectedValue)

    # good data 1D list
    value = [1,2,3]
    expectedValue = np.array([[1],[2],[3]])
    assess_NP_object(__input_check_3x1(value),expectedValue)

    # good data 1D tuple
    value = (1,2,3)
    expectedValue = np.array([[1],[2],[3]])
    assess_NP_object(__input_check_3x1(value),expectedValue)

def assess_NP_object(X,X_expected):
    np.testing.assert_allclose(X,X_expected,atol=ABSOLUTE_TOLERANCE,rtol=RELATIVE_TOLERANCE)

    

