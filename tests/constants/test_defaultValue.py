"""
===================== UNIT TEST FOR DEFAULT SETTINGS ====================
"""


#Import Module
import dragonfly


class Test_DefaultSettings:
    def test_eartModel(self):
        # assert if EarthEllipsoid exists and is a str
        assert hasattr(dragonfly.constants.DEFAULT_SETTINGS,"EarthEllipsoid"), "DEFAULT_SETTINGS has no attribute EarthEllipsoid"
        
        # assert if an str ="WGS84"
        
        assert dragonfly.constants.DEFAULT_SETTINGS.EarthEllipsoid=="WGS84" , "The default model shall be WGS84"