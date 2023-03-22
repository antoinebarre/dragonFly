"""
################# VALIDATION OF FOLDER AND FILE PATHS #################
"""

# EXPORT
__all__ = [
    "validateFile",
    "validateFileExtension",
    "isValidExtension",
    "validateFolder",
]

# IMPORT
import os
import pathlib
from dragonfly.utils.validation import validateInstance, validateTupleInstances
from dragonfly.utils.exception import createErrorMessage


# Definition of deidcated exception
class InvalidFileExtension(Exception):
    "Raised when the file path has not the appropriate extension"
    pass


def validateFile(filepath: str) -> str:
    """check if the file exists and provide the absolute path

    Args:
        filepath (str): file path to asses (relative or absolute)

    Returns:
        str: absolute path
    """

    # chech arguments:
    filepath = validateInstance(filepath, str)

    # Analysis
    try:
        if os.path.isfile(filepath):
            return os.path.abspath(filepath)
    except Exception as e:
        msg = f"impossible to assess the arg1 [{filepath}]"
        raise Exception(msg).with_traceback(e.__traceback__)

    msg = f"The path {filepath} is not an existing file "
    msg = createErrorMessage(
        errorMsg="The path {filepath} shall describe an existing file ",
        expected="Existing file",
        current=f"Not a file [{filepath}]"
    )
    raise ValueError(msg)


def validateFileExtension(
    filepath: str,
    validExtensions: str | tuple[str]
) -> str:
    """Validate the File extension against a list of valid file extension

    Args:
        filepath (str): file path (relative or absolute)
        validExtensions (str | tuple[str]): list of valid extensions
                                            (shall start with ".")

    Returns:
        str: copy of the file path if the extension is correct
    """

    # arguments validation
    filepath = validateInstance(filepath, str)
    tupleExtension = __validateExtensionDefinition(validExtensions)

    # get the extension
    file_extension = pathlib.Path(filepath).suffix

    if file_extension in tupleExtension:
        return filepath

    # raise error

    msg = f"The file [{filepath}] has not the appropriate extension"
    msg = createErrorMessage(
        errorMsg=msg,
        expected=str(tupleExtension),
        current=file_extension,
        )
    raise InvalidFileExtension(msg)


def isValidExtension(
    filepath: str,
    expectedExtensions: str | tuple[str]
) -> bool:
    """check if a path has an appropriate extension

    Args:
        filepath (str): file path to test
        expectedExtensions (str | tuple[str]): list of valid extension
                                               (shall start with ".")

    Returns:
        bool: True if Valid or False else
    """

    # call the __validateFileExtension function
    try:
        filepath = validateFileExtension(filepath, expectedExtensions)
        return True
    except InvalidFileExtension:
        return False
    except Exception as Exc:
        raise Exc


def __validateExtensionDefinition(
        extension2validate: str | tuple[str]) -> tuple[str]:
    """PRIVATE - Validate if a string is an appropriate extensions definition
    (ie. start with a point) and return the same data if OK as a tuple

    Args:
        extension2validate (str | tuple[str]): extension definition to validate

    Returns:
        tuple[str]: tuple of valid extension
    """
    # check if string
    extension2validate = validateTupleInstances(
        data=extension2validate,
        instance=str,
    )  # type: ignore

    if all(elem.startswith('.') for elem in extension2validate):
        return extension2validate  # type: ignore

    # raise error
    msg = createErrorMessage(
        errorMsg=(
            "The extension definition shall start with '.'"
        ),
        expected="example '.py', '.txt'",
        current=f"{extension2validate}"
    )
    raise ValueError(msg)


def validateFolder(folderpath: str) -> str:
    """check if the folder exists and provide the absolute path

    Args:
        folderpath (str): folder path to asses (relative or absolute)

    Returns:
        str: absolute path of the existing folder
    """

    # chech arguments:
    folderpath = validateInstance(folderpath, str)

    # Analysis
    try:
        if os.path.isdir(folderpath):
            return os.path.abspath(folderpath)
    except Exception as e:
        msg = f"impossible to assess the arg1 [{folderpath}]"
        raise Exception(msg).with_traceback(e.__traceback__)

    msg = f"The path {folderpath} is not an existing folder "
    msg = createErrorMessage(
        msg,
        "Existing folder",
        f"Not a folder [{folderpath}]"
    )
    raise ValueError(msg)
