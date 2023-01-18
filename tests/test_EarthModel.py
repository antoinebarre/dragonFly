"""UNIT TEST FOR EARTH MODEL"""

EXPECTED_VALUES = [
    {"name":"WGS84", "a": 6378137.0 , "f": 1/298.257223563, "b":6356752.314245179497563967, "e": 0.081819190842622,"mu":3.986005E+14, "j2":1.08263E-3 # SOURCE : https://fr.wikipedia.org/wiki/WGS_84
    }
]

#Import Module
from dragonfly.constant import EarthModel
import pytest

ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6


def test_EarthModel():

    for model in EXPECTED_VALUES:
        #create EarthModel object

        try:
            model2test = EarthModel(model["name"])
        except Exception as exc:

            assert False, f'creation of the model {model["name"]} raised an error {exc}'
        
       
        #check Earth rotation rate
        msg = f'Inapropriate earth rotational rate'
        assert model2test.earthRotationRate == pytest.approx(7.292115E-5,abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg
       
        #check Earth rotation rate
        msg = f'Inapropriate gravitational constant'
        assert model2test.mu == pytest.approx(model["mu"],abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg
       
        #check Earth rotation rate
        msg = f'Inapropriate second gravitational constant'
        assert model2test.j2 == pytest.approx(model["j2"],abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg
       



        # assert semi major axis
        msg = f'Inapropriate Semi major value for {model["name"]}'
        assert model2test.a== pytest.approx(model["a"],abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg

        # assert semi minor axis
        msg = f'Inapropriate Semi minor value for {model["name"]}'
        assert model2test.b== pytest.approx(model["b"],abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg

        # assert flattening
        msg = f'Inapropriate flattening value for {model["name"]}'
        assert model2test.f== pytest.approx(model["f"],abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg

        # assert excentricity axis
        msg = f'Inapropriate excentricity value for {model["name"]}'
        assert model2test.e== pytest.approx(model["e"],abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg

        
