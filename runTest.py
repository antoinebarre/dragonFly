import pytest
from dragonfly.dev import FolderAnalysis


retcode = pytest.main()
analysis = FolderAnalysis("dragonfly")
