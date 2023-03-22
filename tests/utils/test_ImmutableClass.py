"""
------------- TEST IMMUTABLE CLASS --------------
"""

# Import Module
from dragonfly.utils import ImmutableClass
import pytest


class myClass(ImmutableClass):
    def __init__(self, x):
        self.x = x

        # initalisation with super class
        super().__init__()


class myClass2(ImmutableClass):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # initalisation with super class
        super().__init__()


def test_init():
    try:
        myObject = myClass(3)
        print(myObject.x)

        myObject = myClass2(3, 4)
        print(myObject.x, myObject.y)

    except Exception:
        msg = ("the initialisation of the class and the"
               " get method shall raise no error")
        assert False, msg


def test_immutable():
    """ test if an attributeError is raised"""
    myObject = myClass2(3, 4)

    # test new attribute
    with pytest.raises(AttributeError):
        myObject.z = 3

    # test mutation
    with pytest.raises(AttributeError):
        myObject.x = 3
