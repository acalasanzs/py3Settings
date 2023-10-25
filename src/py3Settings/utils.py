def printObjProps(theObject):
    for property, value in vars(theObject).items():
        print(property, ":", value)
def getWithAttr(list: list, attr: str, name: str):
    """
    Returns the first item in a list of objects that has a specified attribute with a specified value.

    Args:
        list (list): The list of objects to search through.
        attr (str): The value of the attribute to search for.
        name (str): The name of the attribute to search for.

    Returns:
        The first object in the list that has an attribute with the specified name and value, or False if no such object is found.
    """
    for x in list:
        if getattr(x, name) == attr:
            return x
    return False