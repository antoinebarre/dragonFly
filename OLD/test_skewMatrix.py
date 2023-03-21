""" ##################  UNITEST FOR screw matrix  ##################
"""

# MODULE IMPORT
import dragonfly.utils

import numpy as np


ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6


def test_skew_matrix():
    """_summary_a skew matrix shall be equivalent to a vectorial product
    """

    # input
    X = dragonfly.utils. __input_check_3x1(np.array([1, 2, 3]))
    y = dragonfly.utils. __input_check_3x1(np.array([4, 5, 6]))
    expected_res = dragonfly.utils. __input_check_3x1(np.array([-3, 6, -3]))

    # calculate
    res = dragonfly.utils.skew_matrix(X)@y

    # assertion
    np.testing.assert_allclose(res, expected_res,
                               atol=ABSOLUTE_TOLERANCE,
                               rtol=RELATIVE_TOLERANCE)
