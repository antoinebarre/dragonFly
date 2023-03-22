"""UNIT TEST FOR VISUAL FRAMEWORK"""


#Import Module
import dragonfly
import pytest

# ===================== VISUAL FRAMEWORK OBJECT ===================

class Test_Visualframework:
    def test_linesize(self):
        
        # assert if line size exist and is a int
        assert hasattr(dragonfly.constants.VISUAL_FRAMEWORK,"line_size"), "VISUAL_FRAMEWORK has no attribute line_size"
        
        # assert if an int > 0
        line_size = dragonfly.constants.VISUAL_FRAMEWORK.line_size
        assert isinstance(line_size,int) and line_size > 0 , "line_size shall be an int greater strictly than 0"