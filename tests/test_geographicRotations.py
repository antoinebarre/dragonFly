"""UNIT TEST FOR GEOGRAPHIC ROTATIONS"""


# import module
import pytest
import numpy as np

from dragonfly.geography import DCM_ECI2ECEF, dcm_ecef2ned, dcm_ecef2enu, angle2dcm, dcm2angle


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

    M = dcm_ecef2ned(lat,lon)

    #print(M)

    X_ECEF = M.T @ np.reshape(X_NED,(3,-1))

    #assert
    np.testing.assert_array_almost_equal(X_ECEF,X_ECEF_EXPECTED,decimal=4)


class TestECEF2ENU():
    """cf. https://github.com/skulumani/astro/blob/a707ad017f061ef2d465d797b348081dc2bd09bd/astro/tests/test_transform.py"""

    def test_equator_prime_meridian(self):
        latgd = 0
        lon = 0
        dcm_ecef2enu_expected = np.array([[0, 0, 1],
                                          [1, 0, 0],
                                          [0, 1, 0]]).T
        dcm = dcm_ecef2enu(latgd, lon)
        np.testing.assert_allclose(dcm, dcm_ecef2enu_expected)
   
    def test_pole_prime_meridian(self):
        latgd = np.pi/2
        lon = 0        
        dcm_ecef2enu_expected = np.array([[0, 1, 0],
                                          [-1, 0, 0], 
                                          [0, 0, 1]])
        dcm = dcm_ecef2enu(latgd, lon)
        np.testing.assert_array_almost_equal(dcm, dcm_ecef2enu_expected)

    def test_so3(self):
        latgd = np.random.uniform(-np.pi/2, np.pi/2)
        lon = np.random.uniform(-np.pi, np.pi)
        alt = 0
        dcm = dcm_ecef2enu(latgd, lon)
        np.testing.assert_allclose(np.linalg.det(dcm), 1)
        np.testing.assert_array_almost_equal(dcm.T.dot(dcm), np.eye(3,3))
    
    def test_ecef2enu_1(self):
        """ see https://github.com/spacecraft-design-lab-2019/GNC/blob/40455d0324e01691db1c2ce13d2d41b5c5dcaaf7/util_funcs/test/test_frame_conversions.py"""
        lat = 0
        lon = np.pi / 6
        test_vec = np.array([1, 0, 0])
        R_pred = np.array([[-1/2, np.sqrt(3)/2 ,0 ],
                        [0, 0, 1],
                        [np.sqrt(3)/2, 1/2, 0]])
        test_rot_vec = np.array([-1/2, 0, np.sqrt(3)/2])
        np.testing.assert_allclose(dcm_ecef2enu(lat, lon), R_pred, atol=1e-6)  # Python test
        np.testing.assert_allclose(dcm_ecef2enu(lat, lon) @ test_vec, test_rot_vec, atol=1e-6) # checking rotations
   
class test_angle2dcm():    
    def test_angle2dcm_ZYX(self):
        """unit test for angle to dcm with ZYX order

        Data Source: Example 1 generated using book GNSS Applications and Methods
                Chapter 7 library function: eul2Cbn.m (transpose of this used).
                Example 2 found in Performance, Stability, Dynamics, and Control
                of Airplanes, Second Edition (p. 355).

        """
        # Define Euler angles and expected DCMs
        checks = (
            (np.deg2rad([-83, 2.3, 13]), 6,
                np.array([[ 0.121771, -0.991747, -0.040132],
                        [ 0.968207,  0.109785,  0.224770],
                        [-0.218509, -0.066226,  0.973585]])),
            (np.deg2rad([-10, 20, 30]), 4,
                np.array([[ 0.9254,  0.3188,  0.2049],
                        [-0.1632,  0.8232, -0.5438],
                        [-0.3420,  0.4698,  0.8138]]).T),
        )

        for angles, decimal, Rnav2body_expected in checks:
            yaw, pitch, roll = angles

            Rnav2body_computed = angle2dcm(yaw, pitch, roll)
            
            np.testing.assert_almost_equal(Rnav2body_expected, Rnav2body_computed, decimal=decimal)
    
    def test_angle2dcm_error(self):
        "test only ZYX feature is implemented"
        with pytest.raises(NotImplementedError):
            print(angle2dcm(0,0,0,"XYZ"))
            
def test_dcm2angle_ZYX():
    """test dcm2angle with ZYX rotation
    """
    # Define (expected) Euler angles and associated DCM (Rnav2body)
    yaw, pitch, roll = np.deg2rad([-83, 2.3, 13]) # degrees
    
    Rnav2body = np.array([[ 0.121771, -0.991747, -0.040132],
                            [ 0.968207,  0.109785,  0.224770],
                            [-0.218509, -0.066226,  0.973585]])
    
    yaw_C, pitch_C, roll_C = dcm2angle(Rnav2body)

    # Assess
    np.testing.assert_almost_equal([yaw_C, pitch_C, roll_C], [yaw, pitch, roll], decimal=4)

def test_angle2dcm_error():
    "test only ZYX feature is implemented"
    with pytest.raises(NotImplementedError):
        print(dcm2angle(np.ndarray((3,3)),rotationSequence="XYZ"))






        
