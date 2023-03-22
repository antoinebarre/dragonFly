"""
============================ READING TOOLS ============================
"""

# EXPORT
__all__ = [
    "readASCIIFile",
]

# IMPORT PACKAGES
import pathlib
import os


def readASCIIFile(filePath: str | os.PathLike[str]) -> str:
    """PRIVATE - read an existing ASCII File

    Args:
        filePath (str | bytes | os.PathLike): file path (absolute or relative)

    Returns:
        str: contents of the file
    """
    return pathlib.Path(filePath).read_text()
