""" 
# ========================= UNIT TEST FILE READ ========================= #
"""

# IMPORT
import tempfile
import dragonfly


class Test_readASCIIFile():
    
    @staticmethod
    def createfile(filepath,content):
        filepath.parent.mkdir(exist_ok=True) #create a directory 
        filepath.touch() #create a file

        #write to file as normal 
        filepath.write_text(content)
    
    def test_read(self,tmp_path):
        
        f1 = tmp_path / "mydir/myfile.py"
        content = "text to myfile"
        
        # create file
        self.createfile(f1,content)

        #assert
        data = dragonfly.utils.fileIO.readASCIIFile(f1)
        assert data == content
