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
from typing import TypedDict, Literal, Optional

from .snowflake import Snowflake
from .user import User

StickerType = Literal[1, 2]
StickerFormatType = Literal[1, 2, 3]

class _StickerOptional(TypedDict, total=False):
    pack_id: Snowflake
    available: bool
    guild_id: Snowflake
    user: User
    sort_value: int

class Sticker(_StickerOptional):
    id: Snowflake
    name: str
    description: str
    tags: str
    asset: Literal[''] # deprecated
    type: StickerType
    format_type: StickerFormatType


