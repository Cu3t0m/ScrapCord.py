"""
scrapcord
~~~~~~~

A simple API wrapper around Discord API for Python.

The focus of scrapcord is to provide an easy to use, object oriented interface
to interact with Discord API without compromising the quality. Thus, the library
features a very simple and easy to use API design.

:license: MIT
:copyright: scrapcord (c) 2021-present
"""
from . import types, abc, utils
from .asset import *
from .color import *
from .core import *
from .enums import *
from .flags import *
from .user import *
from .guild import *
from .member import *
from .role import *

__author__  = 'NerdGuyAhmad <nerdguyahmad.contact@gmail.com>'
__version__ = '0.0.1'