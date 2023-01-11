"""_UNIT TEST FOR Position Class
"""

# CONSTANT

# MODULE IMPORT
from dragonfly.geography import Position
import pytest

SIMPLE_LIST     = [10,20,30]


@pytest.fixture
def simple_position():
    return Position(SIMPLE_LIST[0],
                      SIMPLE_LIST[1],
                      SIMPLE_LIST[2])
    

def compare_ECEF(position,X_expected):
    """Utility function used to compare a position vs the root data"""

    #extract fields
    X = [position.x,
            position.y,
            position.z]

    axes = ["x","y","z"]
    for idx in range(3):
        assert X[idx]==X_expected[idx] , f"The value of the {axes[idx]} field shall be {X_expected[idx]} [current :{X[idx]}]"

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




def test_fromList_2D():
    """fromArray method shall create a new instance from a 2D array"""
    
    Tested_Array = [SIMPLE_LIST,[2*element for element in SIMPLE_LIST], [3*element for element in SIMPLE_LIST]]

    newPositions = Position.fromList(Tested_Array)

    # assess data type
    assert isinstance(newPositions,list) , f"the output of fromList shall be a Position object [current: {type(Position)}]"

    #assessment

    for idx in range(3):
        compare_ECEF(newPositions[idx],Tested_Array[idx])







