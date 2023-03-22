def test_listdirectory():
    
    try:
        dragonfly.utils.listdirectory(os.getcwd(),extensions=".py",excluded_folders=("venv",".git"))
    except:
        assert False  