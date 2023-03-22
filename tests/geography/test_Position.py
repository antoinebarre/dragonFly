"""
# ===================== UNIT TEST FOR Position Class ==================== #
"""

# MODULE IMPORT
from dragonfly.geography import Position
import pytest
import numpy as np
import math

# CONSTANTS
ABSOLUTE_TOLERANCE  = 1e-12
RELATIVE_TOLERANCE  = 1e-6


SIMPLE_LIST         = [10,20,30]



# from https://www.convertecef.com
LLA4ECEF = [
    {"ECEF": [ 5117118.21, -1087677.05, 3638574.7 ], #meter,meter, meter
    "LLA"  : [35,-12,1234]}, #lat lon alt (deg,deg,m)
    {"ECEF": [ 1193872.96, 1584322.93, -6064737.91 ],
    "LLA"  : [-72,53,22135]}]


@pytest.fixture
def simple_position():
    return Position(SIMPLE_LIST[0],
                      SIMPLE_LIST[1],
                      SIMPLE_LIST[2])
    

############################################################################################

def test_creation(simple_position) -> None:
    """Check creation of the Position object with the appropriate fields
    ie. x, y, z
    Args:
        simple_position (NOne): Fixture
    """
       
    #launch comparisons
    compare_ECEF(simple_position,SIMPLE_LIST)


def test_modif_X(simple_position):
    """x field shall be a float or equivalent (e.g. '1', 1.0, 1"""

    #Error shall be raised (bad value for the interface)
    with pytest.raises(TypeError):
        simple_position.x = [1,2]

    with pytest.raises(TypeError):
        simple_position.x = (1,2)
    
    with pytest.raises(ValueError):
        simple_position.x = "abc"
    
    #No error shall be raised
    try:
        simple_position.x = "1.6"

        assert simple_position.x ==1.6

    except Exception as exc:
        assert False, f"mutation of x raised an exception {exc}"

    
def test_modif_y(simple_position):
    """y field shall be a float or equivalent (e.g. '1', 1.0, 1"""

    #Error shall be raised (bad value for the interface)
    with pytest.raises(TypeError):
        simple_position.y = [1,2]

    with pytest.raises(TypeError):
        simple_position.y = (1,2)
    
    with pytest.raises(ValueError):
        simple_position.y = "abc"
    
    #No error shall be raised
    try:
        simple_position.y = "1.6"
        assert simple_position.y ==1.6
    except Exception as exc:
        assert False, f"mutation of y raised an exception {exc}"

def test_modif_z(simple_position):
    """z field shall be a float or equivalent (e.g. '1', 1.0, 1"""

    #Error shall be raised (bad value for the interface)
    with pytest.raises(TypeError):
        simple_position.z = [1,2]

    with pytest.raises(TypeError):
        simple_position.z = (1,2)
    
    with pytest.raises(ValueError):
        simple_position.z = "abc"
    
    #No error shall be raised
    try:
        simple_position.z = "1.6"
        assert simple_position.z ==1.6
    except Exception as exc:
        assert False, f"mutation of z raised an exception {exc}"
    



############################################################################################

def test_fromList_1D():
    """fromArray method shall create a new instance from a 1D LIST"""
    

    newPosition = Position.fromList(SIMPLE_LIST)

    # assess data type
    assert isinstance(newPosition,Position) , f"the output of fromList shall be a Position object [current: {type(Position)}]"

    #assessment
    compare_ECEF(newPosition,SIMPLE_LIST)

    # assess bad size
    with pytest.raises(ValueError):
        Position.fromList([1,2,3,4])
    
    #bad type
    with pytest.raises(TypeError):
        Position.fromList("a")





def test_fromList_2D():
    """fromArray method shall create a new instance from a 2D array"""
    
    Tested_Array = [SIMPLE_LIST,[2*element for element in SIMPLE_LIST], [3*element for element in SIMPLE_LIST]]

    newPositions = Position.fromList(Tested_Array)

    # assess data type
    assert isinstance(newPositions,list) , f"the output of fromList shall be a Position object [current: {type(Position)}]"

    #assessment

    for idx in range(3):
        compare_ECEF(newPositions[idx],Tested_Array[idx])


def test_toLLA():

    for pos in LLA4ECEF:
        newPos = Position.fromList(pos["ECEF"])

        #check good creation :
        compare_ECEF(newPos,pos["ECEF"])

        #create LLA
        LLA_real = newPos.toLLA()

        #assess LLA
        compare_LLA(LLA_real,pos["LLA"])

def test_FromLLA():
    for pos in LLA4ECEF:
        newPos = Position.fromLLA(np.deg2rad(pos["LLA"][0]),np.deg2rad(pos["LLA"][1]),pos["LLA"][2])

        #compare ECEF
        compare_ECEF(newPos,pos["ECEF"])

############################################################################################

def test_norm():
    """test r property that provides the norm of ECEF coordinates"""
    
    assert Position(1,-2,3).norm == pytest.approx(math.sqrt(1**2+2**2+3**2),
                                    abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE)


def test_toNumpy():

    np.testing.assert_allclose(Position(1,2,3).toNumpy(),np.reshape(np.array([1,2,3]),(3,-1)),
                            rtol=RELATIVE_TOLERANCE,atol=ABSOLUTE_TOLERANCE)

####################################  OPERATION  ####################################

def test_repr():
    #assert repr feature

    assert repr(Position(0,0,0)) == 'ECEF Coordinates:\nx : 0.0\ny : 0.0\nz : 0.0'


def test_equality():

    chk = Position.fromLLA(np.deg2rad(45),np.deg2rad(-45),0)==Position.fromLLA(np.deg2rad(45),np.deg2rad(-45),0)

    assert chk == True

    chk = Position.fromLLA(np.deg2rad(45),np.deg2rad(-44),0)==Position.fromLLA(np.deg2rad(45),np.deg2rad(-45),0)

    assert chk == False

    # check mutation raised error
    with pytest.raises(NotImplementedError):
        Position(0,0,0)==1


def test_sub():
    pos1 = Position(1,2,3)
    pos2 = Position(1,1,1)

    delta = pos1-pos2

    np.testing.assert_allclose(delta.toNumpy(),np.reshape(np.array([0,1,2]),(3,-1)),
                            rtol=RELATIVE_TOLERANCE,atol=ABSOLUTE_TOLERANCE)
            
    # check mutation raised error
    with pytest.raises(NotImplementedError):
        Position(0,0,0)-1



####################################  UTILS  ##############################################

def compare_ECEF(position,X_expected,absTol = ABSOLUTE_TOLERANCE,reltol = RELATIVE_TOLERANCE):
    """Utility function used to compare a position vs the root data"""

    #extract fields
    X = [position.x,
            position.y,
            position.z]

    axes = ["x","y","z"]
    for idx in range(3):
        message = f"{axes[idx]} [{X[idx]}] shall be equal to the expected {axes[idx]} [{X_expected[idx]}]\n" + \
                    f"With the Absolute tolerance : {absTol}  and the relative tolerance {reltol}"

        assert X[idx]== pytest.approx(X_expected[idx],abs=absTol,rel=reltol)  , message

def compare_LLA(LLA_real, LLA_expected,absTol = ABSOLUTE_TOLERANCE,reltol = RELATIVE_TOLERANCE):

    typeLLA = ["Latitude","Longiture","Altidue"]

    # change from rad to deg
    LLA_real = [np.rad2deg(LLA_real[0]),np.rad2deg(LLA_real[1]),LLA_real[2]]

    for idx in range(3):
        message = f"{typeLLA[idx]} [{LLA_real[idx]}] shall be equal to the expected {typeLLA[idx]} [{LLA_expected[idx]}]\n" + \
                    f"With the Absolute tolerance : {absTol}  and the relative tolerance {reltol}"

        assert LLA_real[idx]== pytest.approx(LLA_expected[idx],abs=absTol,rel=reltol) , message











