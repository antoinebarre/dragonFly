"""
######################### DATA TYPE VALIDATION ########################
"""

# EXPORT
__all__ = [
    "validateInstance",
    "validateListInstances",
    "validateTupleInstances",
]

# IMPORT
import typing
import dragonfly


def validateInstance(
    data: typing.Any,
    instances: type | list[type] | tuple[type],
    inheritance: bool = False
) -> typing.Any:
    """validate if a data as the appropriate type

    Args:
        data (Any): data to assess
        instances (type | Tuple[type]): expected types
        inheritance (bool, optional): inheritance activated
            Defaults to False.

    Returns:
        Any: same object as data
    """

    # Nested evaluation function
    def evaluateType(data, listTypes, inheritance) -> bool:
        """Evaluate Type depending of the inheritance option"""
        if inheritance:
            # with inheritance
            return isinstance(data, listTypes)
        else:
            # inheritance is disable
            return type(data) in listTypes

    # check the list of accepted types
    listTypes = validateTupleInstances(
        data=instances,
        instance=type,
    )

    if evaluateType(data, listTypes, inheritance):
        return data

    # raise error
    msg = dragonfly.utils.exception.createErrorMessage(
        errorMsg=("The input shall respected the"
                  f" expected types (inheritance: {inheritance})"),
        expected=str(instances),
        current=f"{data} ({type(data)})",
    )
    raise TypeError(msg)


def validateListInstances(data: typing.Any, instance) -> list:
    """Check if data is a list of instance object

    Args:
        data (any): object to analyze (instance object or
        list of instance objects)
        instance (type): type of the content of the expected list

    Returns:
        list: list of instance objects
    """

    # check instance data type
    if (not isinstance(instance, type)) or instance in (list, set, tuple):
        msg = dragonfly.utils.exception.createErrorMessage(
            errorMsg=((
                "the instance object shall be"
                " a Type object different of list, tuple or set"
            )),
            expected=str(type),
            current=f"{instance} ({type(instance)})",
        )
        raise TypeError(msg)

    if isinstance(data, instance):
        return [data, ]  # force to have a one element tuple
    elif (isinstance(data, list) and
          all(isinstance(elem, instance) for elem in data)):
        return data

    # Raise error
    msg = dragonfly.utils.exception.createErrorMessage(
        errorMsg=(f"The data shall be a {str(instance)}"
                  f" or a list of {str(instance)}"),
        expected=(f"{str(instance)} object "
                  f"or list of {str(instance)} objects"),
        current=data
    )
    raise TypeError(msg)


def validateTupleInstances(
    data: typing.Any | tuple[typing.Any],
    instance: type,
     ) -> tuple:
    """Check if data is a tuple of instance object

    Args:
        data (any): object to analyze
        (instance object or tuple of instance objects)
        instances (type): type of the content of the expected tuple

    Returns:
        tuple: tuple of instance objects
    """

    # check instance data type
    if (not isinstance(instance, type)) or instance in (list, set, tuple):
        msg = dragonfly.utils.exception.createErrorMessage(
            errorMsg=((
                "the instance object shall be"
                " a Type object different of list, tuple or set"
            )),
            expected=str(type),
            current=f"{instance} ({type(instance)})",
        )
        raise TypeError(msg)

    if isinstance(data, instance):
        return (data,)  # force to have a one element tuple
    elif (isinstance(data, tuple) and
          all(isinstance(elem, instance) for elem in data)):
        return data

    # Raise error
    msg = dragonfly.utils.exception.createErrorMessage(
        errorMsg=(f"The data shall be a {str(instance)}"
                  f" or a tuple of {str(instance)}"),
        expectedValue=(f"{str(instance)} object "
                       f"or Tuple of {str(instance)} objects"),
        realValue=str(data)
    )
    raise TypeError(msg)
