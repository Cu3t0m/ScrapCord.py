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

class Colour:
    """
    A class that wraps the integer color values in (r, g, b) like form.

    This class also provides some pre-made classmethods that generates
    different common colors and some from Discord's branding.

    An alias ``Color`` is also available for this class.

    Parameters
    ----------
    value: :class:`int`
        The integer value of color.

    Attributes
    ----------
    r: :class:`int`
        The RED value from `(r, g, b)`
    g: :class:`int`
        The GREEN value from `(r, g, b)`
    b: :class:`int`
        The BLUE value from `(r, g, b)`
    """
    def __init__(self, value: int):
        self.value = value

    @property
    def r(self) -> int:
        return (self.value >> 16) & 255

    @property
    def b(self) -> int:
        return self.value & 255

    @property
    def g(self) -> int:
        return (self.value >> 8) & 255

    def __repr__(self):
        return 'Colour({r}, {g}, {b})'.format(r=self.r, g=self.g, b=self.b)

Color = Colour