"""
############################## ERROR MESSAGE ##############################
"""

# EXPORT
__all__ = [
    "createErrorMessage",
]

# IMPORT PACKAGES


def createErrorMessage(
    errorMsg: str,
    expected: str = "",
    current: str = "",
) -> str:
    """create a generic error message

    Args:
        errorMsg (str): description of the error
        expectedValue (str): expected information
        realValue (str): assessed information

    Returns:
        str: _description_
    """
    msg = (
        f"{errorMsg}\n" +
        f"Expected : {str(expected)}\n" +
        f"Current :  {str(current)}\n"
    )
    return msg
