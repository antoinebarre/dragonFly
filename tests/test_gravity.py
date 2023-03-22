""" ##################  UNITEST FOR GRAVITY  ##################
"""

# MODULE IMPORT
from dragonfly.geography import Position
from dragonfly.gravity import Gravity
import numpy as np



ABSOLUTE_TOLERANCE  = 1e-12
RELATIVE_TOLERANCE  = 1e-6

def test_equator_WGS84():
    #expected value for gravity 

    """ Calculated with
    ee = EarthModel()
    print((ee.mu/ee.a**2)*(1+3/2*ee.j2))
    """
    g_expected = [-9.814197355899799,0 ,0 ]
    g_expected_np =np.reshape(np.array(g_expected),(3,-1))

    pos2test = Position.fromLLA(0,0,0)
  

    g_list =  Gravity.fromLLA(0,0,0).toList()
    np.testing.assert_allclose(g_list,g_expected,
            atol=ABSOLUTE_TOLERANCE,rtol=RELATIVE_TOLERANCE)

    g_np = Gravity.fromLLA(0,0,0).toNumpy()
    np.testing.assert_allclose(g_np,g_expected_np,
            atol=ABSOLUTE_TOLERANCE,rtol=RELATIVE_TOLERANCE)

    #[ i_real == pytest.approx(i_expected, rel=RELATIVE_TOLERANCE, abs=ABSOLUTE_TOLERANCE) for i_real, i_expected in zip(g_list,g_expected)]

def test_NorthPole_WGS84():
    #expected value for gravity 
    """ Calculated with
    ee = EarthModel()
    print((ee.mu/ee.b**2)*(1+3/2*ee.j2*(ee.a/ee.b)**2*-2))
    """
    
    g_expected = [0,0 ,-9.83206684120325 ]
    g_expected_np =np.reshape(np.array(g_expected),(3,-1))
  

    g_list =  Gravity.fromLLA(np.deg2rad(90),0,0).toList()
    np.testing.assert_array_almost_equal(g_list,g_expected)

    g_np = Gravity.fromLLA(np.deg2rad(90),0,0).toNumpy()
    np.testing.assert_array_almost_equal(g_np,g_expected_np )
