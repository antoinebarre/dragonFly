"""_UNIT TEST FOR Position Class
"""

# CONSTANT

# MODULE IMPORT
from dragonfly.geography import Possition
import pytest

SIMPLE_VALUE = [10,20,30]



@pytest.fixture
def simple_position():
    return Possition(SIMPLE_VALUE[0],
                      SIMPLE_VALUE[1],
                      SIMPLE_VALUE[2])
    

def test_creation(simple_position) -> None:
    """Check creation of the Position object with the appropriate fields
    ie. x, y, z
    Args:
        simple_position (NOne): Fixture
    """
    assert simple_position.x==SIMPLE_VALUE[0] , f"The value of the x field shall be {SIMPLE_VALUE[0]} [current :{simple_position.x}"
    assert simple_position.y==SIMPLE_VALUE[1] , f"The value of the y field shall be {SIMPLE_VALUE[1]} [current :{simple_position.y}"
    assert simple_position.z==SIMPLE_VALUE[2] , f"The value of the z field shall be {SIMPLE_VALUE[2]} [current :{simple_position.z}"


