"""UNIT TEST FOR GEOGRAPHIC ROTATIONS"""


# import module
import pytest
import numpy as np

from dragonfly.geography import DCM_ECI2ECEF, DCM_ECEF2NED, Position


ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6
NB_DECIMAL = 8
NB_OBJ = 100



def test_ECI2ECEF()->None:
    """Test Cases for the function DCM_ECI2ECEF
    """

    # assert when dt=0
    np.testing.assert_array_almost_equal(DCM_ECI2ECEF(0),np.identity(3),decimal=NB_DECIMAL)

    #TODO : complete the test cases
    #see https://github.com/geospace-code/pymap3d/blob/main/src/pymap3d/tests/test_eci.py

    pass

def test_ECEF2NED()->None:
    """Test Cases for the DCM_ECEF2NED

    Data Source: Examples 2.1 and 2.4 of Aided Navigation: GPS with High
                     Rate Sensors, Jay A. Farrel 2008

    """

    #reference point:
    lat = np.deg2rad(( 34. +  0./60 + 0.00174/3600)) # North
    lon = np.deg2rad(-(117. + 20./60 + 0.84965/3600)) # West
    alt = 251.702 # [meters]

    X_ECEF_EXPECTED = np.reshape(np.array([0.3808, 0.7364, -0.5592]),(3,-1))
    X_NED  = np.array([0, 0, 1]) # local unit gravity

    M = DCM_ECEF2NED(lat,lon)

    #print(M)

    X_ECEF = M.T @ np.reshape(X_NED,(3,-1))

    #assert
    np.testing.assert_array_almost_equal(X_ECEF,X_ECEF_EXPECTED,decimal=4)





    
