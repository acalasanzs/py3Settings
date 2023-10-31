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
    Examples:
    
    >>> class Person:
        >>> def __init__(self, name, age):
        >>>     self.name = name
        >>>     self.age = age

        >>> people = [
                 Person("Alice", 25),
                Person("Bob", 30),
                 Person("Charlie", 35)
        >>> ]

        >>> # Find the person with name "Bob"
        >>> bob = getWithAttr(people, "Bob", "name")
        >>> print(bob.age)
    """
    for x in list:
        if getattr(x, name) == attr:
            return x
    return False
def has_nested_object(obj):
    def has_tuple(tuple: tuple | list):
        for item in tuple:
            if has_nested_object(item):
                return True
    if isinstance(obj, dict):
        for value in obj.values():
            if isinstance(value, dict):
                return True
            elif isinstance(value, (list, tuple)):
                has_tuple(value)
    elif isinstance(obj, (list, tuple)):
        has_tuple(obj)
    return False
def specialDict(name, value):
    r = {}
    r[name] = value
    return r
def to_objectKeys(list: list):
    new = dict()
    for x in list:
        new[next(iter(x.keys()))] = next(iter(x.values()))
    return new