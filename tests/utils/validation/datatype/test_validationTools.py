""" UNIT TEST FOR VALIDATION TOOLS OF UTILS
"""



# MODULE IMPORT
import dragonfly as dgf
import pytest
import numpy as np
import math



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
                    valOut = dgf.utils.validation.validateInstance(value, testedType)

                    assert valOut is value, f"Error raised for tested type {testedType} and assessed type {assessedType}"
                except Exception:
                    assert False, f"Error raised for tested type {testedType} and assessed type {assessedType}"
            else:
                with pytest.raises(TypeError) as e_info:
                    dgf.utils.validation.validateInstance(value, testedType)

    # test with tuple (OK)
    try:
        testedType = (bool, str)
        assessedType = bool
        value = assessedType()
        valOut = dgf.utils.validation.validateInstance(value, testedType)

        assert valOut is value, f"Error raised for tested type {testedType} and assessed type {assessedType}"

        # with three elements
        testedType = (float, int, tuple)
        assessedType = float
        value = assessedType()
        valOut = dgf.utils.validation.validateInstance(value, testedType)

        assert valOut is value, f"Error raised for tested type {testedType} and assessed type {assessedType}"

        # with inheritance
        testedType = (float, int, tuple)
        assessedType = bool
        value = assessedType()
        valOut = dgf.utils.validation.validateInstance(value, testedType, inheritance=True)

        assert valOut is value, f"Error raised for tested type {testedType} and assessed type {assessedType}"

    except Exception:
        assert False, f"Error raised for tested type {testedType} and assessed type {assessedType}"

    # test with tuple (NOK)
    with pytest.raises(TypeError):
        testedType = (float, int, tuple)
        assessedType = bool
        value = assessedType()
        valOut = dgf.utils.validation.validateInstance(value, testedType, inheritance=False)
        dgf.utils.validation.validateInstance(value, testedType)

    with pytest.raises(TypeError):
        testedType = (float, int)
        assessedType = str
        value = assessedType()
        valOut = dgf.utils.validation.validateInstance(value, testedType, inheritance=False)
        dgf.utils.validation.validateInstance(value, testedType)

    with pytest.raises(TypeError):
        testedType = [float, int]
        assessedType = str
        value = assessedType()
        valOut = dgf.utils.validation.validateInstance(value, testedType, inheritance=False)
        dgf.utils.validation.validateInstance(value, testedType)

    with pytest.raises(TypeError):
        testedType = (float, "a")
        assessedType = str
        value = assessedType()
        valOut = dgf.utils.validation.validateInstance(value, testedType, inheritance=False)
        dgf.utils.validation.validateInstance(value, testedType)
    
    pass

def test_validateTupleInstances():
    
    #bad params
    with pytest.raises(TypeError):
        dgf.utils.validation.validateTupleInstances("toto","str")
    
    with pytest.raises(TypeError):
        dgf.utils.validation.validateTupleInstances("toto",list)
        
    with pytest.raises(TypeError):
         dgf.utils.validation.validateTupleInstances(("str",1),str)
         
    # good value
    expectedValue = ("a",)
    val = dgf.utils.validation.validateTupleInstances("a",str)
    assert val[0] == expectedValue[0]
    assert len(val)==1
    assert isinstance(val,tuple)
    
    expectedValue = ("a","b")
    val = dgf.utils.validation.validateTupleInstances(expectedValue,str)
    assert val is expectedValue
    
 
def test_validateListInstances():
    
    #bad params
    with pytest.raises(TypeError):
        dgf.utils.validation.validateListInstances("toto","str")
    
    with pytest.raises(TypeError):
        dgf.utils.validation.validateListInstances("toto",list)
        
    with pytest.raises(TypeError):
         dgf.utils.validation.validateListInstances(["str",1],str)
         
    # good value
    expectedValue = ["a"]
    val = dgf.utils.validation.validateListInstances("a",str)
    assert val[0] == expectedValue[0]
    assert len(val)==1
    assert isinstance(val,list)
    
    expectedValue = ["a","b"]
    val = dgf.utils.validation.validateListInstances(expectedValue,str)
    assert val is expectedValue    
    