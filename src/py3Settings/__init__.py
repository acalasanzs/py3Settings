#   -------------------------------------------------------------
#   Copyright (c) Albert Calasanz Sallen. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
from .main import AppSettings, Option, Attribute, getWithAttr, addFormatSupport, showFileDefs, printObjProps
from . import proxy
# from . import utils
from . import file
# No hay recursividad
__version__ = "2.1.0"