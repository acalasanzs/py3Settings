
from typing import Callable, List

class Attribute:
    """example:
    ```python
            Define an attribute for the option
            attr1 = Attribute("attr1", int, lambda x: x > 0, default=1)

            Define another attribute for the option
            attr2 = Attribute("attr2", str, lambda x: len(x) > 0, default="default_value")

            Create an option with the attributes
            my_option = Option("my_option", "option_id")
            my_option.append(attr1)
            my_option.append(attr2)```
    
        In this example, we define an Attribute called attr1 with a name of "attr1", a type of int, a validation function that checks if the value is greater than 0, and a default value of 1. We also define another Attribute called attr2 with a name of "attr2", a type of str, a validation function that checks if the length of the value is greater than 0, and a default value of "default_value".

        We then create an Option called my_option with an option name of "my_option", an option ID of "option_id", and append the attr1 and attr2 attributes to it.

        This Option now has two attributes that can be used to validate and process data in the AppSettings class. For example, if we have a settings file with a "my_option" section that contains "attr1" and "attr2" keys, we can use the validateAll method of the AppSettings class to validate the values of these keys using the attr1 and attr2 attributes of the my_option option.
    parameters:
        self: A reference to the instance of the class being created.
        
        attr: A string that represents the name of the attribute.
        
        typ: An optional parameter that specifies the type of the attribute. If this parameter is not provided, the validate parameter must be a callable that takes an object and returns a boolean value indicating whether the object is valid.
        
        validate: An optional parameter that specifies a callable that takes an object and returns a boolean value indicating whether the object is valid. If this parameter is not provided, the typ parameter must be a type object.
        
        default: An optional parameter that specifies the default value of the attribute.
        
        getter -> get: An optional parameter that specifies a callable that returns the value of the attribute. This is useful if the attribute is computed or if it needs to be retrieved from a different location.
        In summary, the Attribute class is used to define an attribute with a name, a type or validation function, a default value, and an optional getter function. The typ and validate parameters are mutually exclusive, and at least one of them must be provided. If typ is provided, the validate function is automatically generated to check if the value is an instance of typ. If validate is provided, it is used to validate the value instead.
    """

    def __init__(
        self,
        attr: str,
        typ: type | None = None,
        validate: Callable[[object], bool] | None = None,
        default: bool = False,
        getter: Callable[[object], object] = None,
    ):
        self.attr = attr
        if typ is None and validate is Callable[[object], bool]:
            self.validate = validate
        elif validate is None and typ is not None:
            self.typ = typ
            self.validate = (
                lambda a: isinstance(a, typ) if not hasattr(self, "get") else self.get
            )
            if getter is not None:
                self.get = getter
        else:
            raise SystemExit("No type!")
        self.default = default
    def get(object: object):
        return object