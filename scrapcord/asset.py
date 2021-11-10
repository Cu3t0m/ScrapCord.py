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
from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import State


class CDNAsset:
    """Represents an asset from Discord's CDN like icons, avatars, emojis etc.

    Attributes
    ----------
    url: :class:`str`
        The URL of the asset.
    key: :class:`str`
        The identification unique key of the asset.
    animated: :class:`bool`
        Whether this asset is animated.
    """
    BASE_CDN_URL: ClassVar[str] = 'https://cdn.discordapp.com'

    def __init__(self, url: str, key: str, animated: bool, state: State):
        self.url = url
        self.key = key
        self.animated = animated
        self._state = state

    def __repr__(self):
        return '<CDNAsset url={} animated={}>'.format(self.url, self.animated)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.url == other.url

    def __str__(self):
        return self.url

    # factory methods

    @classmethod
    def _from_default_avatar(cls, state, disc: int) -> Asset:
        return cls(
            state=state,
            url=f"{cls.BASE_CDN_URL}/embed/avatars/{index}.png",
            key=str(disc % 5),
            animated=False,
        )

    @classmethod
    def _from_avatar(cls, state, user_id: int, avatar_hash: str) -> Asset:
        animated = avatar_hash.startswith("a_")
        fmt = "gif" if animated else "png"
        return cls(
            state=state,
            url=f"{cls.BASE_CDN_URL}/avatars/{user_id}/{avatar_hash}.{fmt}?size=1024",
            key=avatar_hash,
            animated=animated,
        )


    @classmethod
    def _from_banner(cls, state, user_id: int, banner_hash: str) -> Asset:
        animated = banner_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            state,
            url=f"{cls.BASE_CDN_URL}/banners/{user_id}/{banner_hash}.{format}?size=512",
            key=banner_hash,
            animated=animated,
        )


    @classmethod
    def _from_guild_member_avatar(
        cls, state, guild_id: int, member_id: int, avatar_hash: str
    ) -> Asset:
        animated = avatar_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            state=state,
            url=f"{cls.BASE_CDN_URL}/guilds/{guild_id}/users/{member_id}/avatars/{avatar_hash}.{format}?size=1024",
            key=avatar_hash,
            animated=animated,
        )

    @classmethod
    def _from_icon(cls, state, object_id: int, icon_hash: str, path: str) -> Asset:
        return cls(
            state=state,
            url=f"{cls.BASE_CDN_URL}/{path}-icons/{object_id}/{icon_hash}.png?size=1024",
            key=icon_hash,
            animated=False,
        )

    @classmethod
    def _from_guild_image(cls, state, guild_id: int, image: str, path: str) -> Asset:
        return cls(
            state,
            url=f"{cls.BASE_CDN_URL}/{path}/{guild_id}/{image}.png?size=1024",
            key=image,
            animated=False,
        )

    @classmethod
    def _from_guild_icon(cls, state, guild_id: int, icon_hash: str) -> Asset:
        animated = icon_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            state,
            url=f"{cls.BASE_CDN_URL}/icons/{guild_id}/{icon_hash}.{format}?size=1024",
            key=icon_hash,
            animated=animated,
        )

