""" UNIT TEST FOR VALIDATION TOOLS OF UTILS
"""



# MODULE IMPORT
import dragonfly.utils as df
import pytest
import numpy as np
import math
import builtins as b


# CONSTANTS:
BUILTIN_TYPES = [str, int, float, bool, list, tuple, complex, dict]


# ------------------------ __validateInstance -----------------------------

def test__validateInstance() -> None:
    """ Assess the behavior of validateInstance"""

    # Loop over all types for a singleton
    for testedType in BUILTIN_TYPES:
        for assessedType in BUILTIN_TYPES:
            value = assessedType()
            if testedType == assessedType:
                try:
                    valOut = df.__validateInstance(value, testedType)

                    assert valOut is value, f"Error raised for tested type {testedType} and assessed type {assessedType}"
                except Exception:
                    assert False, f"Error raised for tested type {testedType} and assessed type {assessedType}"
            else:
                with pytest.raises(TypeError) as e_info:
                    df.__validateInstance(value, testedType)

    # test with tuple (OK)
    try:
        testedType = (bool, str)
        assessedType = bool
        value = assessedType()
        valOut = df.__validateInstance(value, testedType)

        assert valOut is value, f"Error raised for tested type {testedType} and assessed type {assessedType}"

        # with three elements
        testedType = (float, int, tuple)
        assessedType = float
        value = assessedType()
        valOut = df.__validateInstance(value, testedType)

        assert valOut is value, f"Error raised for tested type {testedType} and assessed type {assessedType}"

        # with inheritance
        testedType = (float, int, tuple)
        assessedType = bool
        value = assessedType()
        valOut = df.__validateInstance(value, testedType, inheritance=True)

        assert valOut is value, f"Error raised for tested type {testedType} and assessed type {assessedType}"

    except Exception:
        assert False, f"Error raised for tested type {testedType} and assessed type {assessedType}"

    # test with tuple (NOK)
    with pytest.raises(TypeError):
        testedType = (float, int, tuple)
        assessedType = bool
        value = assessedType()
        valOut = df.__validateInstance(value, testedType, inheritance=False)
        df.__validateInstance(value, testedType)

    with pytest.raises(TypeError):
        testedType = (float, int)
        assessedType = str
        value = assessedType()
        valOut = df.__validateInstance(value, testedType, inheritance=False)
        df.__validateInstance(value, testedType)

    with pytest.raises(ValueError):
        testedType = [float, int]
        assessedType = str
        value = assessedType()
        valOut = df.__validateInstance(value, testedType, inheritance=False)
        df.__validateInstance(value, testedType)

    with pytest.raises(ValueError):
        testedType = (float, "a")
        assessedType = str
        value = assessedType()
        valOut = df.__validateInstance(value, testedType, inheritance=False)
        df.__validateInstance(value, testedType)
    
    pass
