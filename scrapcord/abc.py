"""
MIT License

Copyright (c) 2021 ScrapCord

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from . import utils

if TYPE_CHECKING:
    from .state import State
    import datetime

class DiscordModel:
    """
    An ABC that implements common operations on a discord model.

    Almost all the classes that represent Discord models inherit
    from this one.
    """
    id: int
    _state: State

    @property
    def created_at(self) -> datetime.datetime:
        """
        :class:`datetime.datetime`: Returns the creation date of this entity. This is determined from the :attr`.id`.
        """
        return utils._get_snowflake_creation_date(self.id)

    def __int__(self):
        return self.id

    def __eq__(self, other: Any):
        return isinstance(other, self) and self.id == other.id

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'