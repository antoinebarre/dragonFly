""" UNIT TEST FOR FiLE VALIDATIO TOOLS OF UTILS
"""

# MODULE IMPORT
import dragonfly
import pytest
import numpy as np
import math
import builtins as b
import tempfile
import os

def test_validatefile():
    
    #create temp file
    temp = tempfile.NamedTemporaryFile()
    assert dragonfly.utils.__validateFile(temp.name) == temp.name , "the file paht exist and shall be equal"
    temp.close() # the file is destroyed
    
    # no file
    with pytest.raises(ValueError) :
        _ = dragonfly.utils.__validateFile(temp.name)
    
    
def test_validateFileExtension():
    """ test the tools to validate extension with a path"""
    
    # bad extension
    with pytest.raises(dragonfly.utils.InvalidFileExtension):
        dragonfly.utils.__validateFileExtension("toto.c",".py")
    
    with pytest.raises(dragonfly.utils.InvalidFileExtension):
        dragonfly.utils.__validateFileExtension("toto.c",(".py",'.f'))
        
    # good extension
    path = dragonfly.utils.__validateFileExtension("toto.py",(".py",'.f'))
    
    assert path == 'toto.py'
    

def test_isvalidExtension():
    """ test the tools to asses is a file has the appropriate extension"""
    assert dragonfly.utils.isValidExtension("toto.c",(".py",'.f')) == False
    assert dragonfly.utils.isValidExtension("toto.f",(".py",'.f')) == True
    
def test_validateExtensionDefinition():
    """ test the validation of the extension inputs"""
    # bad extension
    with pytest.raises(ValueError):
        dragonfly.utils.__validateExtensionDefinition("toto")
        
    with pytest.raises(ValueError):
        dragonfly.utils.__validateExtensionDefinition((".c","f"))
    
    # good extension definition
    
    val_init = (".c",".f")
    val = dragonfly.utils.__validateExtensionDefinition(val_init)
    assert val is val_init
    
def test_validateFolder():
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert dragonfly.utils.__validateFolder(tmpdirname)==tmpdirname
        tmpName = tmpdirname
        
    with pytest.raises(ValueError):
        dragonfly.utils.__validateFolder(tmpName)
        
def test_listdirectory():
    
    try:
        dragonfly.utils.listdirectory(os.getcwd(),extensions=".py",excluded_folders=("venv",".git"))
    except:
        assert False    