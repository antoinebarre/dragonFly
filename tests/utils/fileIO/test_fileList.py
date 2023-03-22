""" 
======================== UNIT TEST FILE LISTING =======================
"""

import dragonfly
import os

def test_listdirectory():
    
    try:
        dragonfly.utils.fileIO.listdirectory(os.getcwd(),extensions=".py",excluded_folders=("venv",".git"))
    except:
        assert False  