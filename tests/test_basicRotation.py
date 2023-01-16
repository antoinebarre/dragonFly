"""UNIT TEST FOR BASIC ROTATION"""


# import module
import pytest
import numpy as np

from dragonfly.utils import rotx,roty,rotz


ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6
NB_DECIMAL = 8
NB_OBJ = 100


@pytest.fixture
def randomAngleArray():
    return np.random.uniform(low=-6*np.pi, #minimal value
                                         high=6*np.pi, #maximum value 
                                         size=NB_OBJ) #number of elements


def test_rotx_determinant(randomAngleArray):
    """The function rotx shall have a determinant equal to 1
    """
    for angle in randomAngleArray:
        det = np.linalg.det(rotx(angle))

        message = f"For an angle of the determinant of a rotation matrix shall be equal to 1.0 [cureent : {det}]"

        assert det == pytest.approx(1.0,abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE) , message

def test_rotx_behaviour():
    
    testCases = [
        [90, np.array([10,0,0]), np.array([10,0,0])],
        [90, np.array([0,9,0]), np.array([0,0,-9])],
        [90, np.array([0,0,4]), np.array([0,4,0])],
        [180, np.array([0,3,0]), np.array([0,-3,0])],
        [270, np.array([0,3,0]), np.array([0,0,3])],
    ]

    for testCase in testCases:
        #behavior :
        X = apply_rotx(testCase[0], testCase[1])
        #assess:
        compare_column_vector(X,testCase[2])

def test_roty_determinant(randomAngleArray):
    """The function roty shall have a determinant equal to 1
    """
    for angle in randomAngleArray:
        det = np.linalg.det(roty(angle))

        message = f"For an angle of the determinant of a rotation matrix shall be equal to 1.0 [cureent : {det}]"

        assert det == pytest.approx(1.0,abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE) , message

def test_roty_behaviour():
    
    testCases = [
        [90, np.array([0,10,0]), np.array([0,10,0])],
        [90, np.array([4,0,0]), np.array([0,0,4])],
        [90, np.array([0,0,4]), np.array([-4,0,0])],
        [180, np.array([3,0,0]), np.array([-3,0,0])],
        [270, np.array([3,0,0]), np.array([0,0,-3])],
    ]

    for testCase in testCases:
        #behavior :
        X = apply_roty(testCase[0], testCase[1])
        #assess:
        compare_column_vector(X,testCase[2])

def test_rotz_determinant(randomAngleArray):
    """The function roty shall have a determinant equal to 1
    """
    for angle in randomAngleArray:
        det = np.linalg.det(rotz(angle))

        message = f"For an angle of the determinant of a rotation matrix shall be equal to 1.0 [cureent : {det}]"

        assert det == pytest.approx(1.0,abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE) , message

def test_rotz_behaviour():
    
    testCases = [
        [90, np.array([0,0,10]), np.array([0,0,10])],
        [90, np.array([4,0,0]), np.array([0,-4,0])],
        [90, np.array([0,4,0]), np.array([4,0,0])],
        [180, np.array([3,0,0]), np.array([-3,0,0])],
        [270, np.array([3,0,0]), np.array([0,3,0])],
    ]

    for testCase in testCases:
        #behavior :
        X = apply_rotz(testCase[0], testCase[1])
        #assess:
        compare_column_vector(X,testCase[2])

#---------------- TOOLS ----------------
def compare_column_vector(X,X_expected,nb_digit= NB_DECIMAL):

    #change 1D to 2D array
    X_expected=np.reshape(X_expected,(3,-1))

    # Assess dimension
    assert X.shape == X_expected.shape , f"The dimension of the vector shall be {X_expected.shape} [current:{X.shape} ]"

    #Assess values
    np.testing.assert_array_almost_equal(X,X_expected,decimal=nb_digit)

def apply_rotx(angle2test,X0):
    """_change to 2d column vector and apply rotation 
    """
    return rotx(np.deg2rad(angle2test)) @ np.reshape(X0,(3,-1))

def apply_roty(angle2test,X0):
    """_change to 2d column vector and apply rotation 
    """
    return roty(np.deg2rad(angle2test)) @ np.reshape(X0,(3,-1))

def apply_rotz(angle2test,X0):
    """_change to 2d column vector and apply rotation 
    """
    return rotz(np.deg2rad(angle2test)) @ np.reshape(X0,(3,-1))