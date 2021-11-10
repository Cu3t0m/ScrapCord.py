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
from typing import Optional, TYPE_CHECKING

from .asset import CDNAsset
from .user import User

if TYPE_CHECKING:
    from .types.member import Member as MemberPayload
    from .guild import Guild

class Member:
    """Represents a member of a :class:`Guild`.

    Attributes
    ----------
    user: :class:`User`
        The user instance of this user.
    nick: Optional[:class:`str`]
        The member's guild avatar. This could be None if user has no specific
        nickname in the guild.
    deaf: :class:`bool`
        Whether the member is deafened in the voice channels.
    mute: :class:`bool`
        Whether the member is muted in the voice channels.
    pending: :class:`bool`
        Whether the user has passed the membership screening or not. ``True`` means
        that user has not passed the membership screening.
    """
    __slots__ = (
        'user', 'nick', 'deaf', 'mute', 'pending',
        '_joined_at', '_roles', '_premium_since', '_avatar', '_permissions',
        '_state', '_guild'
        )
    def __init__(self, data: MemberPayload, guild: Guild, state: State):
        self._state = state
        self._guild  = guild
        self._from_data(data)

    def _from_data(self, data: MemberPayload):
        self.user = User(data['user'], state=self._state)
        self.nick = data.get('nick')
        self.deaf = data.get('deaf', False)
        self.mute = data.get('mute', False)
        self.pending = data.get('pending', False)

        self._joined_at = data.get('joined_at')
        self._roles = data.get('roles', [])
        self._premium_since = data.get('premium_since')
        self._avatar = data.get('avatar')
        self._permissions = data.get('permissions')

    @property
    def guild(self):
        # this property is undocumented because it is unnecessary for
        # general use cases, it is manually exposed to the documentation
        # in events like member_update etc. where it is impossible to
        # figure out the guild the event occured in.
        return self._guild

    @property
    def display_name(self) -> str:
        """
        :class:`str`: Returns the name of member as shown in the guild.

        If the member has a guild username that is returned otherwise the real
        username of the user.
        """
        if self.nick is None:
            return self.user.username

        return self.nick

    @property
    def joined_at(self) -> datetime:
        """:class:`datetime.datetime`: Returns the datetime instance representing the guild joined time of member."""
        return datetime.fromisoformat(self._joined_at)

    @property
    def premium_since(self) -> Optional[datetime]:
        """
        Optional[:class:`datetime.datetime`]: Returns the datetime instance representing the
        time when member used their boost on the guild. This is None if user hasn't boosted
        the guild.
        """
        if self._premium_since:
            return datetime.fromisoformat(self._premium_since)

    @property
    def avatar(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the asset representing the user's
        guild avatar. This returns the guild avatar and would be None if user doesn't
        has any guild specific avatar.

        If you want a shorthand for getting either of guild specific or default avatar,
        Use :attr:`.display_avatar` instead.
        """
        if self._avatar:
            return CDNAsset._from_guild_member_avatar(
                self.guild.id,
                self.user.id,
                self._avatar,
                state=self._state,
            )

    @property
    def display_avatar(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the asset for avatar of member as shown in the guild.

        If the member has a guild specific avatar that is returned otherwise the real
        avatar of the user. In the case in which user doesn't has an avatar, the default
        avatar calculated using discriminator is returned instead.
        """
        if self._avatar is None:
            if self.user.avatar:
                return self.user.avatar
            else:
                return self.user.display_avatar

        return self.avatar



