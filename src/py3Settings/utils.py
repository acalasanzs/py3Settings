def printObjProps(theObject):
    for property, value in vars(theObject).items():
        print(property, ":", value)
def getWithAttr(list: list, attr: str, name: str):
    for x in list:
        if getattr(x, name) == attr:
            return x
    return False