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

import base64
import datetime

class Missing:
    def __eq__(self) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __repr__(self):
        return '<scrapcord.utils.MISSING>'

MISSING = Missing()

def _get_image_data(data: bytes) -> str:

    if data.startswith(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"):
        mime = "image/png"
    elif data[0:3] == b"\xff\xd8\xff" or data[6:10] in (b"JFIF", b"Exif"):
        mime = "image/jpeg"
    elif data.startswith((b"\x47\x49\x46\x38\x37\x61", b"\x47\x49\x46\x38\x39\x61")):
        mime = "image/gif"
    elif data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        mime = "image/webp"
    else:
        raise TypeError("invalid or unsupported image type was provided, valid types are jpeg, png, gif, webp")

    data = base64.b64encode(data).decode("ascii")
    return "data:{0};base64,{1}".format(mime, data)

def _get_snowflake(data: Dict[str, Any], key: str):
    try:
        return int(data[key])
    except (KeyError, TypeError, ValueError):
        return None

def _get_snowflake_creation_date(self, snowflake: int) -> datetime.datetime:
    epoch = ((snowflake >> 22) + 1420070400000) / 1000
    return datetime.datetime.fromtimestamp(epoch)

