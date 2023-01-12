"""
########################  UTILS  ######################## 

collect all the utility fonction of dragonFly

"""

def assertInstance(data_name:str,data:str,expected_Instance:str)->None:
    """PRIVATE TOOLS - used to standardize the error message for Instance assessment in dragonFly

    Args:
        data_name (str): _description_
        data (str): _description_
        expected_Instance (str): _description_
    """

    if not isinstance(data,expected_Instance):
        message = f"{data_name} shall be of the following type(s) : {expected_Instance} [current{type(data)}] "
        raise TypeError(message)
