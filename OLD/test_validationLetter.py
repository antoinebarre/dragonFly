""" 
        UNIT TEST OF THE LETTER VERICATION FEATURES
"""

#Import Module
import dragonfly.utils
import pytest

class TestValidateLetter():
    
    def test_goodLetter(self):
        test = dragonfly.utils.validateLetter(
            data="A",
            letterList = ('A', 'B', 'C', 'D', 'E'),
        )
        
        assert test =="A"
        
    def test_badLetter(self):
        with pytest.raises(ValueError):       
            test = dragonfly.utils.validateLetter(
                data="Z",
                letterList = ('A', 'B', 'C', 'D', 'E'),
            )