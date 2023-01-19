""" 
##############################  TEST DISTANCE CALCULATOR  ################################
"""


#Import Module
from dragonfly.geography import getRange
import pytest
import numpy as np

ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6

VALUE2TEST = [
    [(0.0, 0.0), (0.0, 0.0),0],
    [(0.0, 0.0), (0.0, 1.0),111.319491*1000],
    [(0.0, 0.0), (1.0, 0.0),110.574389*1000],
    [(0.0, 0.0), (0.5, 179.5),19936.288579*1000]
]

def test_getRange():
    """ assess range"""

    for sample in VALUE2TEST:
        lat1    = np.deg2rad(sample[0][0])
        long1   = np.deg2rad(sample[0][1])

        lat2    = np.deg2rad(sample[1][0])
        long2   = np.deg2rad(sample[1][1])

        range_expected = sample[2]

        range_real = getRange(lat1,long1,lat2,long2,nbIter=400)

        msg = f"Test Case : {sample}"

        assert range_real==pytest.approx(range_expected,rel=RELATIVE_TOLERANCE,abs=ABSOLUTE_TOLERANCE), msg

        