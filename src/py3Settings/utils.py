def printObjProps(theObject):
    for property, value in vars(theObject).items():
        print(property, ":", value)
def getWithAttr(list: list, attr: str, name: str):
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