""" 
##############################  TEST CODE CONFORMANCE  ################################
"""


#Import Module
import dragonfly
import pytest
import numpy as np
from collections import namedtuple


# =================== TEST CASES DEFINITION ===========================
singlefunction = namedtuple(
    "singleFunction",
    ("string","cyclomaticComplexity" ))

SINGLE_FUNCTIONS_CASES = [
    singlefunction(
        string='''
def foo(a,b):
    return a+b
        ''',
        cyclomaticComplexity="A"
    ),
    singlefunction(
        string='''
def f(a, b, c):
    if a and b == 4:
        return c ** c
    elif a and not c:
        return sum(i for i in range(41) if i&1)
    elif a+c==3:
        return sum(i*2 for i in range(41) if i&1)
    elif a+c==4:
        return sum(i*18 for i in range(41) if i&1)
    elif a+c==25:
        return sum(i*18 for i in range(41) if i&1)
    elif a+c==250:
        return sum(i*180 for i in range(41) if i&1)
    return a + b
     ''',
        cyclomaticComplexity="C"
    ),
]

# =================== CYCLOMATIC COMPLEXITY ===========================

class Test_CyclomaticComplexity:
    
    @staticmethod
    def createfile(filepath,content):
        filepath.parent.mkdir(exist_ok=True) #create a directory 
        filepath.touch() #create a file

        #write to file as normal 
        filepath.write_text(content)
    
    def test_data(self,tmp_path):
        
        f1 = tmp_path / "mydir/myfile.py"
        content = "text to myfile"
        
        # create file
        self.createfile(f1,content)

        #assert
        obj = dragonfly.dev.CyclomaticComplexity(str(f1))
        assert obj.data == content
        
    def test_isValid(self,tmp_path):
        
        f1 = tmp_path / "mydir/myfile.py"
        
        for singlefunction in SINGLE_FUNCTIONS_CASES:
            # create file
            self.createfile(f1,singlefunction.string)
            
            #assert
            obj = dragonfly.dev.CyclomaticComplexity(str(f1))
            obj.criteria_value="A" # force limit to A
            
            if singlefunction.cyclomaticComplexity>"A":
                assert obj.isValid()==False
            else:
                assert obj.isValid()==True
    
    def test_toString(self,tmp_path):
        f1 = tmp_path / "mydir/myfile.py"
        
        for singlefunction in SINGLE_FUNCTIONS_CASES:
            # create file
            self.createfile(f1,singlefunction.string)
            #assert
            obj = dragonfly.dev.CyclomaticComplexity(str(f1))
            assert isinstance(obj.toString(),str) and obj.toString()!=""
          
            
        
    
        
        
